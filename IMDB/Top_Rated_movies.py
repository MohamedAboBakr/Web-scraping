# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
from bs4 import BeautifulSoup
import requests


class Movie(object):

  def __init__(self, rank, name, link, rating, year):
    self.rank = rank
    self.name = name
    self.link = link
    self.rating = rating
    self.year = year

  def print_movie(self):
    print('Rank : ' + str(self.rank))
    print('Movie name : ' + self.name)
    print('Year : ' + self.year)
    print('Movie rating : ' + self.rating)
    print('Movie Link : ' + self.link)
    print('#############################')


def download_posters(driver, movie_list):

  for movie in movie_list:
    poster_name = movie.name.encode('utf8').replace(':', '')
    driver.get(movie.link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    a = soup.find('div', {'class': 'poster'}).find('a')
    img_link = 'http://www.imdb.com' + a['href']
    driver.get(img_link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    img_src = soup.find('img', {'class': 'pswp__img'})['src']

    poster_file = open('{0}.jpg'.format(poster_name), 'wb')
    poster_file.write(requests.get(img_src).content)
    poster_file.close()


def get_top_rated_movies(url):
  driver = webdriver.PhantomJS(executable_path=r'/usr/lib/phantomjs/phantomjs')
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, 'lxml')

  all_movies = []
  rank = 1
  movies_list = soup.find('tbody', {'class': 'lister-list'}).find_all('tr')

  for movie in movies_list:

    title_col = movie.find('td', {'class': 'titleColumn'})
    title_link = title_col.find('a')
    movie_link = 'https://www.imdb.com' + title_link['href']
    movie_name = title_link.text.strip()
    movie_year = title_col.find('span', {'class': 'secondaryInfo'}).text.strip()
    movie_rating = movie.find('td', {'class': 'ratingColumn imdbRating'}).find('strong').text.strip()

    new_movie = Movie(rank, movie_name, movie_link, movie_rating, movie_year)
    all_movies.append(new_movie)

    rank += 1

  download_posters(driver, all_movies)
  driver.quit()
  return all_movies


def print_movies(movies_list):

  for movie in movies_list:
    movie.print_movie()


top_rated_movies = get_top_rated_movies('https://www.imdb.com/chart/top?ref_=nv_mv_250_6')
print_movies(top_rated_movies)

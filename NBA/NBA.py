# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
from bs4 import BeautifulSoup
from player_info import player_info


class Player(object):
  def __init__(self, name, link):
    self.name = name
    self.link = link

  def add_info(self, info, videos, bio):
    self.info = info
    self.videos = videos
    self.bio = bio

  def print_player(self):
    print('Player Name: ' + self.name + '\n')

    print('Player Link: ' + self.link + '\n')
    print('Stats & Info : ')
    for key, value in zip(self.info.keys(), self.info.values()):
      print('\t\t' + key + '\t---->\t' + value)

    print('\n')
    print('Latest Videos : (Text --> Link)')
    for video in self.videos:
      print('\t\t' + video[0] + '\t---->\t' + video[1])

    print('\n')
    print(self.bio)
    print('#################################################################################')


def get_players():
  driver = webdriver.PhantomJS(executable_path=r'/usr/lib/phantomjs/phantomjs')
  url = 'http://www.nba.com/players'
  driver.get(url)

  html_doc = driver.page_source
  soup = BeautifulSoup(html_doc, 'lxml')

  a_tags = soup.find_all('a', {'class': 'row playerList'})
  All_players = []

  for a in a_tags:
    name = a['title']
    link = 'http://www.nba.com' + a['href']
    new_player = Player(name, link)
    All_players.append(new_player)

  for player in All_players:
    info, videos, bio = player_info(driver, player.link)
    player.add_info(info, videos, bio)

  driver.quit()
  return All_players


def print_players(players_list):

  for player in players_list:
    player.print_player()


players_list = get_players()
print_players(players_list)

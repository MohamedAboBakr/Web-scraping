# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
from bs4 import BeautifulSoup


def player_info(driver, url):
  driver.get(url)

  html_doc = driver.page_source
  soup = BeautifulSoup(html_doc, 'lxml')

  info = {}
  latest_videos = []

  # get player stats
  player_detail = soup.find('player-detail')
  stats = player_detail.find('section', {'class': 'nba-player-season-career-stats'})
  if stats != None:
    table = stats.find('table', {'role': 'grid'})
    rates = table.find('thead').find_all('abbr')
    values = table.find('tbody').find_all('tr')[1].find_all('td')

    for rate, value in zip(rates, values):
      value = value.text
      value = value.replace("\n", "")
      value = value.strip()
      key = rate['title'] + '(' + rate.text + ')'
      info[key] = value

  # get height & weight
  details2 = soup.find_all('p', {'class': 'nba-player-vitals__top-info-metric'})
  if details2 != None:
    height = details2[0].text
    height = height.replace("/", "")
    height = height.strip()
    height = height.replace("\n", "")

    weight = details2[1].text
    weight = weight.replace("/", "")
    weight = weight.strip()
    weight = weight.replace("\n", "")

    info['Height'] = height
    info['Weight'] = weight

  # get more info
  details3 = soup.find('section', {'class': 'nba-player-vitals__bottom menu vertical'})
  if details3 != None:
    list_ = details3.find_all('li')
    for li in list_:
      key_value = li.find_all('span')
      key = key_value[0].text
      key = key.strip()
      key = key.replace("/", "")

      value = key_value[1].text
      value = value.strip()
      info[key] = value

  # get player videos
  videos_list = soup.find('section', {'class': 'nba-player-video-scroll row'})
  if videos_list != None:
    videos_list = videos_list.find_all('a')
    for video in videos_list:
      href = 'http://www.nba.com' + video['href']
      video_text = video.find('footer').find('p').text
      video_text = video_text.replace("\n", "")
      video_text = video_text.strip()
      latest_videos.append((video_text, href))

  # get player Bio
  player_bio = soup.find('section', {'class': 'nba-player-detail__bio'})
  if player_bio != None:
    player_bio = player_bio.text
    player_bio = player_bio.strip()

  return info, latest_videos, player_bio

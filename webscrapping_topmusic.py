# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 20:30:10 2020

@author: Ivan Mello
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 20:09:32 2020

@author: Ivan Mello
"""
import time
import requests
import pandas as pd
import re
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#This variable will be used to determine song name
artist_name='queen'
index_start = len(artist_name) + 2

# Importing HTML content
url = "https://www.vagalume.com.br/" + artist_name + "/"

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(url)
time.sleep(10)
element = driver.find_element_by_id('alfabetMusicList')
topMusicList_html = element.get_attribute('outerHTML')
driver.quit()

# Parsing the HTML content using BeautifulSoup
topMusic = BeautifulSoup(topMusicList_html,'lxml')
topMusic = topMusic.prettify()

#Converting str to list separating words by a simple space
def Convert(string):
    li = list(string.split("\n"))
    return li

#Function to remove line breaks in a list
def Remove_lb(list):
    li = []
    for x in list:
        li.append(x.replace('\n',''))
    return li

#Function to remove '#play' in a list
def Remove_play(list):
    li = []
    for x in list:
        li.append(x.replace('#play',''))
    return li

#Function to remove '<a href="' in a list
def Remove_final(list):
    li = []
    for x in list:
        li.append(x.replace('        <a href="',''))
    return li

#Function to remove '<a href="' in a list
def Remove_final2(list):
    li = []
    for x in list:
        li.append(x.replace('">',''))
    return li

#Start creating the list of html song names
topMusic_list = list(filter(None, Convert(topMusic)))
topMusic_list2 = Remove_lb(topMusic_list)
topMusic_list3 = Remove_play(topMusic_list2)
topMusic_list = [ x for x in topMusic_list3 if "<a href=" in x ]
topMusic_list = Remove_final(topMusic_list)
allMusic_list = Remove_final2(topMusic_list)

#Start creating the list of song names to save lyrics file
song_names = []
for x, name in enumerate(allMusic_list, start=0):
    index_stop = allMusic_list[x].index('.html')
    song_name = allMusic_list[x][int(index_start):int(index_stop)]
    song_names.append(song_name)

#Creating dataframe of all songs
df_allsongs=pd.DataFrame({'song_name': song_names})
df_allsongs['song_html_address'] = allMusic_list

#Exporting allsongs_file
df_allsongs.to_csv(r'C:\Users\Ivan Mello\Documents\93 - Webscrapping - Songs\Queen\allsongs_' + artist_name + '.csv', sep='|', encoding='utf-8', index=False)


#Iterating inside df_allsongs to extract lyrics from all songs of the artist
for index, row in df_allsongs.iterrows():
    song_html = row['song_html_address']
    song_name = row['song_name']
    
    # Importing HTML content from the song
    url = "https://www.vagalume.com.br" + song_html

    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)
    
    driver.get(url)
    time.sleep(10)
    element = driver.find_element_by_id('lyrics')
    lyrics_html = element.get_attribute('outerHTML')
    driver.quit()
    
    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(lyrics_html,'lxml')
    lyrics = soup.prettify()
    #print(lyrics)
    
    #Converting str to list separating words by a simple space
    def Convert(string):
        li = list(string.split(" "))
        return li
    
    #Function to remove line breaks in a list
    def Remove(list):
        li = []
        for x in list:
            li.append(x.replace('\n',''))
        return li
    
    #Start creating the list
    lyrics_list = list(filter(None, Convert(lyrics)))
    lyrics_list2 = Remove(lyrics_list)
    lyrics_final = [x for x in lyrics_list2 if all(y not in x for y in '<>=')]
    
    #Transforming the list into a dataframe
    numbers = range(1,len(lyrics_list2))
    sequence_of_numbers = [number for number in numbers]
    df_lyrics=pd.DataFrame({'lyrics': lyrics_final})
    df_lyrics['artist'] = artist_name
    df_lyrics['song_name'] = song_name
    df_lyrics['word_order'] = np.arange(1,len(df_lyrics)+1)
    
    #Creating file name
    filename = '\\' + artist_name + '_' + song_name + '.csv'
    
    #Exporting lyrics into a csv_file
    df_lyrics.to_csv(r'C:\Users\Ivan Mello\Documents\93 - Webscrapping - Songs\Queen' + filename, sep='|', encoding='utf-8', index=False)
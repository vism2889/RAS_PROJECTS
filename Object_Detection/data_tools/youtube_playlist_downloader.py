#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 08/17/2020
# FILENAME: youtube_playlist_downloader.py
#
###############################################################################
# INFO:
# - Script to download all videos from a youtube playlist
# - Most of the code came from the attatched link, small updates were needed: 
#   https://www.geeksforgeeks.org/python-program-to-download-complete-youtube-playlist/
# 



import bs4 as bs 
import sys 
import urllib.request 
from PyQt5.QtWebEngineWidgets import QWebEnginePage 
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtCore import QUrl 
import pytube # library for downloading youtube videos 
  
  
class Page(QWebEnginePage): 
    def __init__(self, url): 
        self.app = QApplication(sys.argv) 
        QWebEnginePage.__init__(self) 
        self.html = '' 
        self.loadFinished.connect(self._on_load_finished) 
        self.load(QUrl(url)) 
        self.app.exec_() 
  
    def _on_load_finished(self): 
        self.html = self.toHtml(self.Callable) 
        print('Load finished') 
  
    def Callable(self, html_str): 
        self.html = html_str 
        self.app.quit() 
  
  
links = [] 
  
  
def exact_link(link): 
    vid_id = link.split('=') 
    # print(vid_id) 
    str = "" 
    for i in vid_id[0:2]: 
        str += i + "="
  
    str_new = str[0:len(str) - 1] 
    index = str_new.find("&") 
  
    new_link = "https://www.youtube.com" + str_new[0:index] 
    return new_link 
  
  
url = "https://www.youtube.com/playlist?list=PLfev9Q0BAHzR2Fikl7xFnb1BOyHc3UJ9o"
# Scraping and extracting the video 
# links from the given playlist url 
page = Page(url) 
count = 0
  
soup = bs.BeautifulSoup(page.html, 'html.parser') 
for link in soup.find_all('a', id='thumbnail'): 
      
    # not using first link because it is 
    # playlist link not particular video link 
    if count == 0:  
        count += 1
        continue
    else: 
        vid_src = link.get('href','')  
        # print(vid_src) 
        # keeping the format of link to be 
        # given to pytube otherwise in some cases 
        new_link = exact_link(vid_src)  
          
        # error might occur due to this 
        # print(new_link) 
          
        # appending the link to the links array 
        links.append(new_link)  
  
# print(links) 
  
# downloading each video from 
# the link in the links array 
for link in links:  
    yt = pytube.YouTube(link) 
      
    # Downloaded video will be the best quality video 
    stream = yt.streams.filter(progressive=True, 
                file_extension='mp4').order_by( 
                'resolution').desc().first()  
    try: 
        stream.download() 
        # printing the links downloaded 
        print("Downloaded: ", link)  
    except: 
        print('Some error in downloading: ', link) 
import requests
from bs4 import BeautifulSoup
import re

class Crawler():
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.response.encoding = 'UTF-18'
        self.soup = BeautifulSoup(self.response.text, 'html5lib')
        self.options = {}

    def select_crawler(self):
        p = re.compile('^https?://([a-zA-Z.0-9]*)')
        host = p.findall(self.url)[0]

        if host == 'www.11st.co.kr':
            from .elevenST import ElevenST 
            return ElevenST(self.url)
        elif host == '':
            return ''

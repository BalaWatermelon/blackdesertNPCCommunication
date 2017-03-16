# coding=utf-8
from bs4 import BeautifulSoup
import requests


class Calculate():
    web = requests.get('http://bd.youxidudu.com/npc/20170102/4266.html')
    soup = BeautifulSoup(web.content, 'html.parser')
    print(soup.find_all('div', class_='card_tie')
          [0].text)

if __name__ == '__main__':
    Calculate()

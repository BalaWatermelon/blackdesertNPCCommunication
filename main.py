from bs4 import BeautifulSoup
import requests


class Calculate():
    web = requests.get('http://bd.youxidudu.com/npc/20170102/4266.html')
    soup = BeautifulSoup(web.text.encode('utf8'), 'html.parser')
    print(soup.find('.card_tie').text)

if __name__ == '__main__':
    Calculate()

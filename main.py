# coding=utf-8
from bs4 import BeautifulSoup
import requests


class Calculate():
    web = requests.get('http://bd.youxidudu.com/npc/20170102/4266.html')
    soup = BeautifulSoup(web.content, 'html.parser')
    print(soup.find_all('div', class_='card_tie')
          [0].text)

    href = "http://bd.youxidudu.com/e/action/ListInfo.php?ph=1&mid=19&tempid=32&fenlei_id_c=152"

    web = requests.get(href)
    soup = BeautifulSoup(web.content, 'html.parser')
    for item in soup.find_all('tr', class_='read'):
        try:
            id = item.find_all('td')[0]

            # Check if it is npc. npc has only three digits
            if len(id.text.strip()) == 3:
                name = item.find_all('td', class_='k_title')[0].a.text.strip()
                print(name)
                # This is an npc, get link for it.
                href = item.find_all('td', class_='k_title')[0].a['href']
                npc = requests.get(href)
                npcSoup = BeautifulSoup(npc.content, 'html.parser')
                print(npcSoup.find_all(
                    'span', class_='c_xingqudu')[0].text.strip())
                print(npcSoup.find_all(
                    'span', class_='c_haogandu')[0].text.strip())

        except:
            print('no id')


if __name__ == '__main__':
    Calculate()

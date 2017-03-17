# coding=utf-8
import sys
import requests
import re
from bs4 import BeautifulSoup


class Calculate():

    def __init__(self):
        self.characterName = ''
        self.intrestNpcList = []

    # Crawl target character's intrest npc's name, intrest and feeling.
    def crawl(self):
        # Retrieve target character's name
        # Temperary fixed url
        # TODO: Retrieve from a list of target character data.
        web = requests.get('http://bd.youxidudu.com/npc/20170102/4266.html')
        soup = BeautifulSoup(web.content, 'html.parser')
        print(soup.find_all('div', class_='card_tie')
              [0].text)
        # Temperary uses fixed url.
        # TODO: Replace with crawl data from webpage.
        href = "http://bd.youxidudu.com/e/action/ListInfo.php?ph=1&mid=19&tempid=32&fenlei_id_c=152"

        web = requests.get(href)
        soup = BeautifulSoup(web.content, 'html.parser')
        for item in soup.find_all('tr', class_='read'):
            try:
                character_id = item.find_all('td')[0].text.strip()

                # Check if it is npc. npc has only three digits
                if len(character_id) == 3:
                    npc_name = item.find_all(
                        'td', class_='k_title')[0].a.text.strip()
                    # This is an npc, get link for it.
                    href = item.find_all('td', class_='k_title')[0].a['href']
                    npc_webpage = requests.get(href)
                    npcSoup = BeautifulSoup(
                        npc_webpage.content, 'html.parser')

                    # Retrieve Intrest for npc
                    npc_intrest = npcSoup.find_all(
                        'span', class_='c_xingqudu')[0].text.split()[1]
                    print(npc_intrest)

                    # Retrieve Feeling for npc
                    npc_feeling = npcSoup.find_all(
                        'span', class_='c_haogandu')[0].text.strip()
                    # Check if it is fixed vaule or ranged value.
                    # TODO: Fix splitting problem to get correct high low
                    # value.
                    print(re.split('~～', npc_feeling.split("：")[1]))
                    '''
                    if '~' in npc_feeling:
                        npc_feeling_low, npc_feeling_high = npc_feeling.split()[
                            1].split(sep='~')
                    else:
                        npc_feeling_high, npc_feeling_low = npc_feeling, npc_feeling


                    print(npc_name, npc_intrest_low, npc_intrest_high,
                          npc_feeling_low, npc_feeling_high)
                          '''
                    # Append data to list
                    # self.intrestNpcList.append(
                    #   [npc_name, npc_intrest_low, npc_intrest_high, npc_feeling_low, npc_feeling_high])

            except:
                print(sys.exc_info())

    def listAllIntrestInfo(self):
        if not self.intrestNpcList:
            print('No npc in list.')
        else:
            for npc in self.intrestNpcList:
                '{:10}興趣度{:2}~{:2} 好感度{:2}~{:2}'.format(
                    npc[0], npc[1], npc[2], npc[3], npc[4])

    def splitWave(self, target):
        low, high = target.split()[1].split(sep='~')
        return low, high

if __name__ == '__main__':
    myCalculate = Calculate()
    myCalculate.crawl()
    myCalculate.listAllIntrestInfo()

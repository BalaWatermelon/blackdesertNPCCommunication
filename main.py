# coding=utf-8
import sys
import requests
import re
from bs4 import BeautifulSoup


class Calculate():

    def __init__(self):
        self.characterName = ''
        self.characterInterest = 0
        self.characterFeelingLow = 0
        self.characterFeelingHigh = 0
        self.intrestNpcList = []
        self.talkingTurns = 3

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
                    # Get npc name
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

                    # Retrieve Feeling for npc
                    npc_feeling = npcSoup.find_all(
                        'span', class_='c_haogandu')[0].text.strip()
                    # Check if it is fixed vaule or ranged value.
                    # TODO: Fix splitting problem to get correct high low
                    # value.
                    npc_feeling_low, npc_feeling_high = re.split(
                        '~|～', npc_feeling.split("：")[1])

                    # Append data to list
                    self.intrestNpcList.append(
                        [npc_name, npc_intrest, npc_feeling_low, npc_feeling_high])

            except KeyboardInterrupt:
                sys.exit()
            except:
                a = sys.exc_info()
        self.calculateBestMatch()

    def calculateBestMatch(self):
        while self.talkingTurns>0:
            if self.getCharacterValue() and self.getTalkingTarget():
                self.printBestList()
            self.talkingTurns-=1
        self.reset()
        self.calculateBestMatch()

    def printBestList(self):
        tmpNpcList = self.intrestNpcList
        for npc in tmpNpcList:
            npc[1] = int(npc[1])-int(self.characterInterest)
            avgFeeling = (int(npc[2])+int(npc[3]))/2
            npc.append(avgFeeling)
        print(tmpNpcList)

    def getCharacterValue(self):
        while self.characterInterest is 0:
            self.characterInterest = raw_input('>>> Interest:')
            try:
                int(self.characterInterest)
            except:
                self.characterInterest = 0
        while self.characterFeelingLow is 0:
            self.characterFeelingLow = raw_input('>>> FeelingLow:')
            try:
                int(self.characterFeelingLow)
            except:
                self.characterFeelingLow = 0
        while self.characterFeelingHigh is 0:
            self.characterFeelingHigh = raw_input('>>> FeelingHigh:')
            try:
                int(self.characterFeelingHigh)
            except:
                self.characterFeelingHigh = 0
        print('Interset:{} Low:{} High:{}')
        return True

    def getTalkingTarget(self):
        while self.getTalkingTarget is None:
            # TODO: Fool proof for input
            self.getTalkingTarget = raw_input('>>> Target(ex.g3, b2):')
        return True

    def listAllIntrestInfo(self):
        if not self.intrestNpcList:
            print('No npc in list.')
        else:
            for npc in self.intrestNpcList:
                print('{:_<15}興趣度{:_<5} 好感度{:_<5}~{:_<5}'.format(
                    npc[0], npc[1], npc[2], npc[3]))

    def reset(self):
        self.characterName = ''
        self.characterInterest = 0
        self.characterFeelingLow = 0
        self.characterFeelingHigh = 0
        self.intrestNpcList = []
        self.talkingTurns = 3


if __name__ == '__main__':
    myCalculate = Calculate()
    # Add options for selecting npc.
    myCalculate.crawl()
    myCalculate.listAllIntrestInfo()

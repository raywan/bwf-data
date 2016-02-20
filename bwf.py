import numpy as np
import pandas as pd
import re
import requests
import time
import random
from bs4 import BeautifulSoup

base = 'http://bwfbadminton.com/rankings/2/bwf-world-rankings'

targets = {
    'ms': '6/men-s-singles',
    'ws': '7/women-s-singles',
    'md': '8/men-s-doubles',
    'wd': '9/women-s-doubles',
    'xd': '10/mixed-doubles'
}

user_agents = [
  'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
  'Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00',
  'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
  'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
  'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko',
  'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; el-GR)',
  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
  'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
  'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
  'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
  'Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00',
  'Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.8.131 Version/11.11',
  'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'
]        

headers = {
  'Accept-Encoding': 'deflate',
}

def getBWFRankings(category, year, week):
    link = '{base}/{target}/{year}/{week}?rows_per_page=5000'.format(base=base,target=targets[category], year=year, week=week)

    headers['User-Agent'] = random.choice(user_agents)
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    downs = soup.find_all('img', {'src': re.compile('down\.png')})
    for d in downs:
        d.parent.find('span', class_='ranking-change').string = '-' + d.parent.find('span', class_='ranking-change').string

    done = False
    while (not done):
        try: 
            table = soup.find('table', class_='tblRankingLanding')
            table = pd.read_html(str(table))[0]
            done = True
        except:
            print "ERROR IN TABLE. TRYING AGAIN IN 60 seconds"
            time.sleep(60)
            headers['User-Agent'] = random.choice(user_agents)
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            downs = soup.find_all('img', {'src': re.compile('down\.png')})
            for d in downs:
                d.parent.find('span', class_='ranking-change').string = '-' + d.parent.find('span', class_='ranking-change').string

    return table

def saveData(table, name):
    table.to_csv(name, encoding='utf-8')

def getWeeks(category):
    print "GETTING WEEKS FOR {c}...".format(c=category)
    result = []
    link = '{base}/{target}'.format(base=base, target=targets[category])
    headers = {'Accept-Encoding': 'deflate'}
    headers['User-Agent'] = random.choice(user_agents)
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    weeks = soup.find('select', {'id': 'ranking-week'}).find_all('option')
    for w in weeks:
        result.append(w['value'].split('--'))
    print "DONE"
    return result

def main():
    weeks = getWeeks('wd')
    for w in weeks:
        print 'Retrieving from {target}: {year}--{week}'.format(target='wd', year=w[0], week=w[1])
        name = 'data/wd/bwf_{target}_{year}w{week}.csv'.format(target='wd', year=w[0], week=w[1])
        saveData(getBWFRankings('wd', w[0], w[1]), name)
        print 'Done'
        print 'Resting for 20 seconds...'
        time.sleep(30)

main()

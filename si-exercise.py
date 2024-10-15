#si-exercise

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import time

# A function to collect lego sets from search results on brickset.com
def collectLegoSets(startURL):
    # Add headers to imitate a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }

    myPage = requests.get(startURL)

    parsed = BeautifulSoup(myPage.text)

    a = [i for i in parsed.find_all('article')]


    newData = []

    for i in a:
        row = []

        row.append(i.h1.text)
        try:

            row.append(float(re.search(r'(\u20AC)(\d+.\d+)', i.find('dt', text="RRP").find_next_sibling().text, re.UNICODE).groups()[1]))
        except:

            row.append(np.nan)

        try:
            row.append(float(re.search(r'(\d+)', i.find('dt', text="Pieces").find_next_sibling().text, re.UNICODE).groups()[0]))
        except:

            row.append(np.nan)

        try:
            row.append(float(re.search(r'(\d+)', i.find('dt', text="Minifigs").find_next_sibling().text, re.UNICODE).groups()[0]))
        except:

            row.append(np.nan)


        newData.append(row)

    newData = pd.DataFrame(newData, columns = ['Set', 'Price_Euro', 'Pieces','Minifigs'])

    try:
        nextPage = parsed.find('li', class_="next").a['href']
    except:
        nextPage = None

    if nextPage:

        time.sleep(2)

        return pd.concat([newData, collectLegoSets(nextPage)], axis=0)

    else:
        return newData

lego2019 = collectLegoSets("https://brickset.com/sets/year-2019")
lego2019.to_csv('lego2019.csv', index=False)

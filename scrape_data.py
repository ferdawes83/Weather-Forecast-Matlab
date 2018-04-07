import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from calendar import monthrange

years = [2014,2015,2016,2017]
rows = []
for year in years:
    for month in range(1,13):
        day = monthrange(year,month)
        url = 'https://www.wunderground.com/history/airport/WMKK/' + str(year) + '/' + str(month) + '/' + str(day[1]) +'/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        table = soup.find("table",attrs={"class":"obs-table responsive"})
        for r in table.find_all('tr'):
            rows.append([''.join(val.text.split()) for val in r.find_all('td')])
        with open('weatherdata.csv', 'w+') as f:
           writer = csv.writer(f)
           writer.writerows(row for row in rows if row)

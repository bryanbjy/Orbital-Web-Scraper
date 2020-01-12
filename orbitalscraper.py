##web-scraping

import requests
import re
from bs4 import BeautifulSoup
from datetime import date, timedelta

page = requests.get('https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches')
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table', class_ = 'wikitable')
rows = table.find_all('tr')

dict = {} ## data structure to contain date and number of distinct launches
seenFirstLaunch = True ## boolean variable to determine if at least one payload is reported as one of three keywords

for row in rows:
    if(row.find('span', class_='nowrap') != None):
        temp = row.find('span', class_='nowrap').get_text()
        blocks = row.find_all('td')
        dateSplit = re.split('(\d+)',blocks[0].get_text()) ##split at change of alphabet to number
        if(dateSplit[0] == ''):
            currDate = dateSplit[1] + dateSplit[2]
        else:
            currDate = dateSplit[0]

        if(temp == currDate): ##if first box of row contains the date update
            actualDate = temp
            seenFirstLaunch = False

    if(not seenFirstLaunch):
        blocks = row.find_all('td')
        for block in blocks: ## check each block in row for the three keywords
            text = block.get_text().split('[')[0].split('\n')[0]
            if(text == 'Operational' or text == 'Successful' or text == 'En route'):
                if actualDate in dict:
                    dict[actualDate] += 1
                else:
                    dict[actualDate] = 1
                seenFirstLaunch = True

## write into csv

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

startDate = date(2019, 1, 1)
endDate = date(2019, 12, 31)

delta = endDate - startDate

f = open('output.csv','w')
for i in range(delta.days + 1):
    date = startDate + timedelta(days=i)
    dateStr = str(date.day) + ' ' + str(months[date.month])
    if dateStr in dict: ## if date is in hashtable write date and corresponding value pair
        line = str(date) + 'T00:00:00+00:00' + ',' + str(dict[dateStr]) + '\n'
        f.write(line)
    else: ## otherwise write date and value of 0
        line = str(date) + 'T00:00:00+00:00' + ',' + str(0) + '\n'
        f.write(line)
f.close()

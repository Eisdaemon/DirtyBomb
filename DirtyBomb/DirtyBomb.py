#! python3
# DirtyBomb.py - Searches random terms on google to hide your identity between fake requests

import bs4, requests, os, random, time, re
import urllib.parse
from urllib.parse import urlparse
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
#Gets the random line for the question


def getQuestions(afile):
    line = random.choice(open(afile).readlines())
    return line
#Formats the questions neatly for a google search
def formatForSearch():
    line = getQuestions('E:\\Dokumente\\Dataset\\Questions.txt')
    #Splits into Words
    words = line.split()
    #Rejoins with plus(Google Searches work with pluses not with spaces)
    searchTerm = '+'.join(words)
    return searchTerm

#Searches on google and clicks on links
def googleSearch():
    websites = []
    #Ties new and old together
    query = formatForSearch()
    url = f"https://google.com/search?q={query}"
    #Open Website Shabang
    headers = {"user-agent": USER_AGENT}
    res = requests.get(url, headers=headers)
    res.raise_for_status
    #Find everything
    if res.status_code == 200:
        soup = bs4.BeautifulSoup(res.content, "html.parser")
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            websites.append(link)
    return websites
    
def openWebsites(sites):
    num = random.randint(0, 4)
    if(num > 0):
        url = random.choice(sites)
        res = requests.get(url)
        res.raise_for_status
    if(num > 1):
        url1 = random.choice(sites)
        res = requests.get(url1)
        res.raise_for_status      
    if(num > 2):
        url2 = random.choice(sites)
        res = requests.get(url2)
        res.raise_for_status    

def connected():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False

def execution():
    while True:
        if(connected):
            try:
                openWebsites(googleSearch())
                time.sleep(rand.randint(1800, 3600))
            except:
                time.sleep(rand.randint(1800, 3600))
                

execution()
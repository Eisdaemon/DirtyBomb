#! python3
# DirtyBomb.py - Searches random terms on google to hide your identity between fake requests

import bs4, requests, os, random, time, re, logging
import urllib.parse
from urllib.parse import urlparse
from pathlib import Path
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61"
#Gets the random line for the question
logging.basicConfig(filename = 'E:\\Dokumente\\TestPython\\dirtyBombLog.txt', level=logging.INFO, format=' %(asctime)s - %(levelname) s - %(message)s')
logging.debug('Start of programm')
form_data={}
def loginData():
    # Fill in your details here to be posted to the login form.
    p = Path('E:\Dokumente\TestPython\googleLogIn.txt')
    #Open Data
    loginData = open(p)
    Mail = loginData.readline()
    psw = loginData.readline()
    loginData.close()
    #Cut \n from Mail
    Mail = Mail.rstrip("\n")
    form_data={'Email': Mail, 'Passwd': psw}

def getQuestions(afile):
    line = random.choice(open(afile).readlines())
    logging.debug(f'Extracted Line:"{line}"')
    return line
#Formats the questions neatly for a google search
def formatForSearch():
    line = getQuestions('E:\\Dokumente\\Dataset\\Questions.txt')
    #Splits into Words
    words = line.split()
    #Rejoins with plus(Google Searches work with pluses not with spaces)
    searchTerm = '+'.join(words)
    logging.debug(f'Searchterm:"{searchTerm}"')
    return searchTerm

#Searches on google and clicks on links
def googleSearch():
    #Dont know for what, but was on stackoverflow
    post = "https://accounts.google.com/signin/challenge/sl/password"
    #makes sure that you are getting logged ot or smth. like that
    with requests.Session() as s:
        #Logs you in
        soup = bs4.BeautifulSoup(s.get("https://accounts.google.com/ServiceLogin?elo=1").text, "html.parser")
        #Fills data in
        for inp in soup.select("#gaia_loginform input[name]"):
            if inp["name"] not in form_data:
                form_data[inp["name"]] = inp["value"]
    #Does stuff
    s.post(post, form_data)
    websites = []
    #Ties new and old together
    query = formatForSearch()
    url = f"https://google.com/search?q={query}"
    logging.info(f'Search for:"{url}"')
    #Open Website Shabang
    headers = {"user-agent": USER_AGENT}
    res = s.get(url, headers=headers)
    res.raise_for_status
    #Find everything
    if res.status_code == 200:
        soup = bs4.BeautifulSoup(res.content, "html.parser")
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            websites.append(link)
    return websites


def openWebsites(sites):
    #Dont know for what, but was on stackoverflow
    post = "https://accounts.google.com/signin/challenge/sl/password"
    #makes sure that you are getting logged ot or smth. like that
    with requests.Session() as s:
        #Logs you in
        soup = bs4.BeautifulSoup(s.get("https://accounts.google.com/ServiceLogin?elo=1").text, "html.parser")
        #Fills data in
        for inp in soup.select("#gaia_loginform input[name]"):
            if inp["name"] not in form_data:
                form_data[inp["name"]] = inp["value"]
    #Does stuff
    s.post(post, form_data)
    num = random.randint(0, 4)
    if(num > 0):
        url = random.choice(sites)
        res = s.get(url)
        res.raise_for_status
        logging.info(f'Clicked on:"{url}"')
    if(num > 1):
        url1 = random.choice(sites)
        res = s.get(url1)
        res.raise_for_status      
        logging.info(f'Clicked on:"{url1}"')
    if(num > 2):
        url2 = random.choice(sites)
        res = s.get(url2)
        res.raise_for_status    
        logging.info(f'Clicked on:"{url2}"')

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
                logging.info('Succesfull execution')
                time.sleep(random.randint(1800, 3600))
            except:
                logging.error('Unseccesfull execution')
                time.sleep(random.randint(1800, 3600))
execution()
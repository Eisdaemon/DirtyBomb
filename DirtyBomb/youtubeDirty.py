import bs4, requests, os, random, time, re, logging, DirtyBomb, json
import urllib.parse
from urllib.parse import urlparse
from pathlib import Path
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61"
logging.basicConfig(filename = 'E:\\Dokumente\\TestPython\\dirtyBomblog.txt', level=logging.INFO, format=' %(asctime)s - %(levelname) s - %(message)s')
form_data={}
youtubeFile = 'E:\\Dokumente\\Dataset\\youtube.txt'

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
    globals().update(form_data={'Email': Mail, 'Passwd': psw})

def getTitle():
    #Gets the title
    yId = DirtyBomb.getQuestions(youtubeFile)
    yId = yId.rstrip("\n")
    #Stackoverflow
    youtubeAddress = 'https://www.youtube.com/watch?v='+yId+'&pbjreload=101'
    params = {"format": "json", "url": youtubeAddress}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return(data['title'])

def format():
    line = getTitle()
    words = line.split()
    #Rejoins with plus(Google Searches work with pluses not with spaces)
    searchTerm = '+'.join(words)
    try:
        logging.debug(f'Searchterm:"{searchTerm}"')
    except:
        logging.info('The log did not work correctly :(')
    return searchTerm

def sucheNachVideo():
    #Creates search Url
    url = "https://www.youtube.com/results?search_query="+format()
    try:
        logging.info(f'Youtube Url:"{url}"')
    except:
        logging.info('The log did not work correctly :(')
    #Fills in Login
    loginData()
    #Search
    post = "https://accounts.google.com/signin/challenge/sl/password"
    #makes sure that you are getting logged ot or smth. like that
    with requests.Session() as s:
        #Logs you in
        soup = bs4.BeautifulSoup(s.get("https://accounts.google.com/ServiceLogin?elo=1").text, "html.parser")
        #Fills data in
        for inp in soup.select("#gaia_loginform input[name]"):
            if inp["name"] not in form_data:
                form_data[inp["name"]] = inp["value"]
    s.post(post, form_data)
    headers = {"user-agent": USER_AGENT}
    res = s.get(url, headers=headers)
    res.raise_for_status

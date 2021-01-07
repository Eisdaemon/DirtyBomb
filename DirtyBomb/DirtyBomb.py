#! Python 3.8
# DirtyBomb - It is impossible not to generate data in the, therefore it generates a lot of confusing data
import bs4, requests, os, random, time, re, logging, urllib.parse, json
from urllib.parse import urlparse
from pathlib import Path
#Import of all Modules
#Initialize Log in Data

#Searching is always through the adress, rather than the search fields
class DirtyBomb:

    def __init__(self, youtubeFile, SearchFile, googleAccount, USER_AGENT):
        #Set loggging up
        logging.basicConfig(filename = 'E:\\Dokumente\\TestPython\\dirtyBomblog.txt', level=logging.INFO, format=' %(asctime)s - %(levelname) s - %(message)s')
        #Data
        self.youtubeFile = youtubeFile
        self.SearchFile = SearchFile
        self.googleAccount = googleAccount
        #User Agent to ensure web funtionallity
        self.USER_AGENT = USER_AGENT
        #Fill in the login_data

    #Get Log in data from a .txt. file
    def loginData(self):
        p = Path(self.googleAccount)
        #Open Data
        loginData = open(p)
        Mail = loginData.readline()
        psw = loginData.readline()
        loginData.close()
        #Cut \n from Mail
        Mail = Mail.rstrip("\n")
        form_data={'Email': Mail, 'Passwd': psw}
        return form_data
    
    #Get a Question/Video etc. from a .txt file
    def getDirt(self, file):
        line = random.choice(open(file).readlines())
        logging.debug(f'Extracted Line:"{line}"')
        return line

    #Open a session loggeg into google
    def googleLogin(self):
        #Gets the form_data
        form_data = DirtyBomb.loginData(self)
        #Understand for the some parts, but it should work
        post = "https://accounts.google.com/signin/challenge/sl/password"
        #All in one Session
        with requests.Session() as s:
            #Logs you in
            soup = bs4.BeautifulSoup(s.get("https://accounts.google.com/ServiceLogin?elo=1").text, "html.parser")
            #Fills data in
            for inp in soup.select("#gaia_loginform input[name]"):
                if inp["name"] not in form_data:
                    form_data[inp["name"]] = inp["value"]
        #Does stuff
        s.post(post, form_data)
        return s

    def formatForSearch(self, filename):
        #Accepts either a filename from goofle search or a string for youtube
        if type(filename) == str:
            line = filename
        else:
            line = DirtyBomb.getDirt(self, filename)
        #Splits into Words
        words = line.split()
        #Rejoins with plus(Google Searches work with pluses not with spaces)
        searchTerm = '+'.join(words)
        try:
            logging.debug(f'Searchterm:"{searchTerm}"')
        except:
            logging.info('The log did not work correctly :(')
        return searchTerm
    #Google Part of the Bomb

    #Format the Dirt for the search
    
    
    #The actual search
    def googleSearch(self):
        s = DirtyBomb.googleLogin(self)
        websites = []
        #Now it gets the search words
        query = DirtyBomb.formatForSearch(self, self.SearchFile)
        url = f"https://google.com/search?q={query}"
        logging.info(f'Search for:"{url}"')
        #Open Website
        headers = {"user-agent": self.USER_AGENT}
        res = s.get(url, headers=headers)
        res.raise_for_status
        #Find everything
        #Checks if the status is ok
        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.content, "html.parser")
        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                websites.append(link)
        return websites
    
    #Opens between one and three websites which are results
    def googleBombExecution(self):
        s = DirtyBomb.googleLogin(self)
        sites = DirtyBomb.googleSearch(self)
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

    #DirtyYouTube - Now youtube searches are following

    #The only dataset which I found contains only the ids - nobody searches for Id. Therefore this scraps the title, without beeing logged in, in Order to sarch later more like a human
    def getTitle(self):
        #Gets the title
        yId = DirtyBomb.getDirt(self, self.youtubeFile)
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
            return(DirtyBomb.formatForSearch(self,data['title']))

    #Actual seach for the video - I do not know how much is tracked without clicking afterwards on a video, therfore "clicking" is an upcomming feature
    def youtubeBombExecution(self):
        #Creates search Url
        url = "https://www.youtube.com/results?search_query="+DirtyBomb.getTitle(self)
        try:
            logging.info(f'Youtube Url:"{url}"')
        except:
            logging.info('The log did not work correctly :(')
        s = DirtyBomb.googleLogin(self)
        headers = {"user-agent": self.USER_AGENT}
        res = s.get(url, headers=headers)
        res.raise_for_status

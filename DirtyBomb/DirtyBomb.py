#! Python 3.8
# DirtyBomb - It is impossible not to generate data in the, therefore it generates a lot of confusing data
import bs4, requests, os, random, time, re, logging, urllib.parse, json, re
from urllib.parse import urlparse
from pathlib import Path
#Selenium Stuff
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver import ActionChains 
from selenium.webdriver.chrome.options import Options 
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
        if 'Dataset\Questions.txt' in filename:
           line = DirtyBomb.getDirt(self, filename)
        else:
            line = filename
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

#Twitterbot - Largely from GeeksforGeeks - Based on Selenium
class Twitterbot: 
  
    def __init__(self,twitterLogin): 
  
        """Constructor 
  
        Arguments: 
            twitterLogin {string} -- where the Twitter Log in Data is stored
        """
        self.twitterLogin = twitterLogin
        # initializing chrome options 
        chrome_options = Options() 
  
        # adding the path to the chrome driver and  
        # integrating chrome_options with the bot 
        self.bot = webdriver.Chrome( 
            executable_path = 'E:\Dokumente\TestPython\chromedriver_win32\chromedriver', 
            options = chrome_options 
        ) 

    #Scrap Daily Trends
    def getHashtags(self):
        CleanRegex = re.compile(r'>(.*)<')
        CleanZweiRegex = re.compile(r'[\w\d\s_.-]+')
        #All Links are Saved here         
        allSites=[]
        #Website where trends are from
        url = 'https://twitter-trends.iamrohit.in/united-states'
        #Standard Scrapping of all Links
        headers= {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61"}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', href=True, target='_blank'):
            allSites.append(a)
        for i in range(len(allSites)):
            #Clean Up with Regex
            current = str(allSites[i])
            mo = CleanRegex.search(current)
            current = mo.group()
            mo2 = CleanZweiRegex.search(current)
            current = mo2.group()
            allSites[i] = current
        cleanSites = []
        for j in range(len(allSites)):
            #Remove All other Link Titles; Super Annoying
            current = allSites[j]
            if 'Youtube Trends' in current or 'Google Trends' in current or 'Coupons' in current or 'Age Calculator' in current or 'Play DuckHunt Game' in current or 'Play 2048 Game' in current or ' YouTube Trends ' in current:
                current = ''
            else:
                cleanSites.append(current)
        hashtag = random.choice(cleanSites)
        logging.info(f'Hashtag:"{hashtag}"')
        return(hashtag)
    def twitterLogin(self):
            p = Path(self.twitterLogin)
            #Open Data
            loginData = open(p)
            Mail = loginData.readline()
            Username = loginData.readline()
            psw = loginData.readline()
            loginData.close()
            #Cut \n from Mail
            Mail = Mail.rstrip("\n")
            return Mail, Username, psw
    def login(self, method): 
        """ 
            Method for signing in the user  
            with the provided email and password. 
        """
        
        bot = self.bot 
        mail, username, psw = Twitterbot.twitterLogin(self)
        # fetches the login page 
        bot.get('https://twitter.com/login') 
        # adjust the sleep time according to your internet speed 
        time.sleep(3) 
  
        email = bot.find_element_by_xpath( 
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input'
        ) 
        password = bot.find_element_by_xpath( 
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input'
        ) 
        if method == 1:
            # sends the email to the email input 
            email.send_keys(mail)
            logging.debug('Logged into Twitter - With Mail')
        else:
            #Now try with username
            email.send_keys(username)
            logging.debug('Logged into Twitter - With Username')
        # sends the password to the password input 
        password.send_keys(psw) 
        # executes RETURN key action 
        password.send_keys(Keys.RETURN) 
        #If Login in with Mail failed
        time.sleep(2)
        #Was the Log In succesfull?
        if bot.current_url == 'https://twitter.com/login?email_disabled=true&redirect_after_login=%2F':
            logging.debug('Mail Log In failed')
            Twitterbot.login(self, 2)
        time.sleep(2) 
  
    def like_retweet(self): 
  
        """ 
        This function automatically retrieves 
        the tweets and then likes and retweets them 
  
        Arguments: 
            hashtag {string} -- twitter hashtag 
        """
  
        bot = self.bot 
        logging.debug('Get Hashtag')
        hashtag = Twitterbot.getHashtags(self)
        logging.debug('Bot for Like_retweet initalized')
        # fetches the latest tweets with the provided hashtag 
        bot.get( 
            'https://twitter.com/search?q=%23'+hashtag+'&src=trend_click&vertical=trends'
        ) 
  
        time.sleep(3) 
  
        # using set so that only unique links 
        # are present and to avoid unnecessary repetition 
        links = set()  
  
        # obtaining the links of the tweets 
        for _ in range(3): 
            # executing javascript code  
            # to scroll the webpage 
            bot.execute_script( 
                'window.scrollTo(0, document.body.scrollHeight)'
            ) 
  
            time.sleep(4) 
  
            # using list comprehension  
            # for adding all the tweets link to the set 
            # this particular piece of code might 
            # look very complicated but the only reason 
            # I opted for list comprehension because is 
            # lot faster than traditional loops 
            [ 
                links.add(elem.get_attribute('href')) 
                for elem in bot.find_elements_by_xpath("//a[@dir ='auto']") 
            ] 
        i = 0
        # traversing through the generated links 
        for link in links:
            #Nothing for the Hashtag was found, another run is required
            #if len(links ==6):
            #    break
            #    Twitterbot.like_retweet(self)
            # opens individual links 
            #print(len(links))
            bot.get(link) 
            time.sleep(4)
            if i == 3:
                break
            i += 1
            try: 
                # retweet button selector 
                bot.find_element_by_css_selector( 
                    '.css-18t94o4[data-testid ="retweet"]'
                ).click() 
                # initializes action chain 
                actions = ActionChains(bot) 
                # sends RETURN key to retweet without comment 
                actions.send_keys(Keys.RETURN).perform() 
  
                # like button selector 
                bot.find_element_by_css_selector( 
                    '.css-18t94o4[data-testid ="like"]'
                ).click() 
                # adding higher sleep time to avoid 
                # getting detected as bot by twitter 
                logging.info(f'Liked and retweeted:"{link}"')
                time.sleep(10) 
            except: 
                time.sleep(2) 
  
        # fetches the main homepage 
        bot.get('https://twitter.com/') 
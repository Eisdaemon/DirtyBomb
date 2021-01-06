import time, random, DirtyBomb, logging
import urllib.parse
from urllib.parse import urlparse

#Checks Connections
def connected():
    try:
        urllib.request.urlopen('http://google.com')
        time.sleep(1800)
        return True
    except:
        logging.error('No Connection')
        return False
#Executes everything
def execution():
    #Initializes the bomb
    db = DirtyBomb.DirtyBomb(
        'E:\\Dokumente\\Dataset\\youtube.txt',
        'E:\\Dokumente\\Dataset\\Questions.txt',
        'E:\Dokumente\TestPython\googleLogIn.txt',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61"
        )
    while(True):
        if(connected):
            try:
                db.youtubeBombExecution()
                time.sleep(random.randint(450, 900))
            except:
                logging.error('Unseccesfull execution - Or some unloggable chars maybe')
                time.sleep(random.randint(450, 900))
            try:
                db.googleBombExecution()
                time.sleep(random.randint(450, 900))
            except:
                logging.error('Unseccesfull execution')
                time.sleep(random.randint(450, 900))
execution()
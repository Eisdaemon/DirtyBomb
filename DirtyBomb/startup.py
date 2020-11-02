import time, random, DirtyBomb, youtubeDirty, logging
import urllib.parse
from urllib.parse import urlparse
logging.basicConfig(filename = 'E:\\Dokumente\\TestPython\\dirtyBombLog.txt', level=logging.INFO, format=' %(asctime)s - %(levelname) s - %(message)s')
def connected():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        time.sleep(1800)
        return True
    except:
        return False
def execution():
    DirtyBomb.loginData()
    while True:
        if(connected):
            try:
                DirtyBomb.openWebsites(DirtyBomb.googleSearch())
                logging.info('Succesfull execution')
                time.sleep(random.randint(450, 1800))
                youtubeDirty.sucheNachVideo()
                time.sleep(random.randint(450, 1800))
            except:
                logging.error('Unseccesfull execution')
                time.sleep(random.randint(450, 3600))
execution()
#to avoid circular import
from __future__ import unicode_literals
import math
import os
import unicodedata
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def prRed(skk,end="\n"): print("\033[91m{}\033[00m" .format(skk),end=end)
def prGreen(skk,end="\n"): print("\033[92m{}\033[00m" .format(skk),end=end)
def prYellow(skk,end="\n"): print("\033[93m{}\033[00m" .format(skk),end=end)
def prCyan(skk,end="\n"): print("\033[96m{}\033[00m" .format(skk),end=end)
def prLightPurple(skk,end="\n"): print("\033[94m{}\033[00m" .format(skk),end=end) 
def prPurple(skk,end="\n"): print("\033[95m{}\033[00m" .format(skk),end=end)

load_dotenv()
PLAYLIST_FILE_NAME = os.getenv("PLAYLIST_FILE_NAME", "")

def deleteBadCharacters(text) -> str:
    text = text.replace(",","")
    text = text.replace("’","'")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def printBar(current, total): #i am geniuenly proud of this function
    '''prints a bar to see how the download is coming along'''
    percentage = round(100*current/total,2)
    bartotalstring = f'\rValidating Files ||{percentage, 2}%'
    fill = '█'
    terminalSize = os.get_terminal_size().columns
    length = terminalSize - len(bartotalstring) if terminalSize - len(bartotalstring) > 10 else 10
    printEnd = ""
    filledLength = int(math.floor((float(percentage)/100)*length))
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\rValidating Files |{bar}| {percentage}%', end = printEnd)
    
def validateFiles(files):
    deletefiles = []
    length = len(files)
    for j,i in enumerate(files,start =1 ):
        printBar(j, length)
        try:
            audio = MP3(i, ID3=EasyID3)
            if audio == {}: deletefiles.append(i)
        except:
            deletefiles.append(i)
    for k in deletefiles:
        os.remove(k)
#to avoid circular import
from __future__ import unicode_literals
import os
import unicodedata
from dotenv import load_dotenv

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
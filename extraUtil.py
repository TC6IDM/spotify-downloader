from __future__ import unicode_literals
import json
import os
import unicodedata
from dotenv import load_dotenv
import jsonpickle
from YoutubeSong import YoutubeSong
from spotdl.types.song import Song
from pytube import Search
from typing import List
import re

def prRed(skk,end="\n"): print("\033[91m{}\033[00m" .format(skk),end=end)
def prGreen(skk,end="\n"): print("\033[92m{}\033[00m" .format(skk),end=end)
def prYellow(skk,end="\n"): print("\033[93m{}\033[00m" .format(skk),end=end)
def prCyan(skk,end="\n"): print("\033[96m{}\033[00m" .format(skk),end=end)
def prLightPurple(skk,end="\n"): print("\033[94m{}\033[00m" .format(skk),end=end) 
def prPurple(skk,end="\n"): print("\033[95m{}\033[00m" .format(skk),end=end)

MAX_SEARCH_DEPTH = 5

load_dotenv()

PLAYLIST_FILE_NAME = os.getenv("PLAYLIST_FILE_NAME", "")
def removeBrackets(text) -> str:
    cleanerTrackName = re.sub('\<.*?\>', '', text)
    cleanerTrackName = re.sub('\[.*?\]', '', cleanerTrackName)
    cleanerTrackName = re.sub('\{.*?\}', '', cleanerTrackName)
    cleanerTrackName = re.sub('\(.*?\)', '', cleanerTrackName)
    return cleanerTrackName
    
def removePunctuation(text) -> str:
    cleanerTrackName = re.sub(r'[^\w\s]', '', text)
    cleanerTrackName = re.sub("\s\s+", " ", cleanerTrackName)
    return cleanerTrackName

def cleanTrackName(text) -> str:
    cleanerTrackName = removeBrackets(text)
    cleanerTrackName = removePunctuation(cleanerTrackName)
    cleanerTrackName = cleanerTrackName.strip()
    return cleanerTrackName.lower()

def removeBrackets(text) -> str:
    cleanerTrackName = re.sub('\<.*?\>', '', text)
    cleanerTrackName = re.sub('\[.*?\]', '', cleanerTrackName)
    cleanerTrackName = re.sub('\{.*?\}', '', cleanerTrackName)
    cleanerTrackName = re.sub('\(.*?\)', '', cleanerTrackName)
    return cleanerTrackName

def deleteBadCharacters(text) -> str: 
    text = text.replace(",","")
    text = text.replace("’","'")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def get_videos(song: Song) -> List[YoutubeSong]:
    '''Gets and returns the video ID and Title (as seen on youtube)'''        
    intitleSTANDARD = "#intitle official audio #intitle high quality #intitle HQ"
        
    if (song.explicit): 
        intitleSTANDARD += " #intitle explicit"
    trackArtistsPlain = [deleteBadCharacters(artist) for artist in song.artists]
    trackArtists = "/".join(trackArtistsPlain)
    song.youtubeSearch = trackArtists+" - "+song.name+" "+intitleSTANDARD
    enoughResults = False
    retries = 0
    while not enoughResults:
        print("Searching Youtube for "+song.youtubeSearch)
        youtubeVideos = []
        s = Search(song.youtubeSearch)
        if (len(s.results)<MAX_SEARCH_DEPTH):
            # prRed(f'Found {len(youtubeVideos)} results, not enough, retrying with different query',end='\r')
            match retries:
                case 0:
                    # prYellow(f'\nQUERY: {song.youtubeSearch}\nRetrying with only the original artist')
                    song.youtubeSearch = song.artist+" - "+song.name+" "+intitleSTANDARD
                case 1:
                    # prYellow(f'\nQUERY: {song.youtubeSearch}\nRetrying with only the original artist and without brackets in the track name')
                    song.youtubeSearch = song.artist+" - "+removeBrackets(song.name)+" "+intitleSTANDARD
                case 2:
                    # prYellow(f'\nQUERY: {song.youtubeSearch}\nRetrying with only the original artist and without brackets in the track name and without #intitle')
                    song.youtubeSearch = song.artist+" - "+removeBrackets(song.name)
                case _:
                    pass
                    # prRed(f'\nRetry: {retries} Song Skipped')
            retries+=1
            # prYellow(f'NEW QUERY: {song.youtubeSearch}')
            continue
                
        enoughResults = True 
        for i,r in enumerate(s.results):
            # prGreen(f'Found {i+1} of {len(s.results)} results {round(100*(i+1) / len(s.results),2)}%                        ',end='\r')
            thisYoutubeSong = YoutubeSong(song,r)
            youtubeVideos.append(thisYoutubeSong)
        
        return youtubeVideos,song
            
def getBestVideo(youtubeVideos: List[YoutubeSong],song: Song) -> str:
    found = None
    difference = 0
    possibleSongList: List[YoutubeSong] =[]
    oneT=10**12
    while found is None:
        
        for i,currentYoutubeVideo in enumerate(youtubeVideos):
            # print(f'\nFinding Best Video {i} of {MAX_SEARCH_DEPTH} {100*i/MAX_SEARCH_DEPTH}%                        ',end='\r')
            currentYoutubeVideo.weight = currentYoutubeVideo.views
            timediff = abs(int(currentYoutubeVideo.song.duration)-int(currentYoutubeVideo.length))
            currentYoutubeVideo.notWithinTimeLimit = timediff > difference+(int(currentYoutubeVideo.song.duration)*0.05)
            currentYoutubeVideo.badTitle = not currentYoutubeVideo.isNotBad()
            currentYoutubeVideo.nameInTitle = cleanTrackName(deleteBadCharacters(currentYoutubeVideo.song.name)) in currentYoutubeVideo.title.lower()
            currentYoutubeVideo.goodNameInTitle = currentYoutubeVideo.isVeryGood()
            currentYoutubeVideo.closeToTime = timediff<=difference
            if (currentYoutubeVideo.notWithinTimeLimit or currentYoutubeVideo.badTitle): continue
                
            if currentYoutubeVideo.nameInTitle: currentYoutubeVideo.weight += oneT
            if currentYoutubeVideo.goodNameInTitle: currentYoutubeVideo.weight += oneT
            if currentYoutubeVideo.closeToTime: currentYoutubeVideo.weight += oneT 
            possibleSongList.append(currentYoutubeVideo)
        song.youtubeSongs = possibleSongList
        if (len(possibleSongList)!=0):
            possibleSongList.sort(key=lambda x: x.weight, reverse=True)
            song.bestMatch = possibleSongList[0]
            saveToDebug(song)
            return song.bestMatch.youtubeLink
        # prRed(f'No suitable video found for {currentYoutubeVideo.song.name} within {difference} ms of the origninal',end='\r')
        difference+=1000
        
def saveToDebug(song: Song):
    json_object = jsonpickle.encode(song)
    if not os.path.exists("C:\\Users\\Owner\\Desktop\\spotify-downloader\\debug"):
        os.makedirs("C:\\Users\\Owner\\Desktop\\spotify-downloader\\debug")
    with open("C:\\Users\\Owner\\Desktop\\spotify-downloader\\debug"+song.name, "w") as outfile:
        outfile.write(json.dumps(json.loads(json_object), indent=4))
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
    trackArtistsPlain = [deleteBadCharacters(artist) for artist in song.artists]
    trackArtists = "/".join(trackArtistsPlain)
    song.youtubeSearch = trackArtists+" - #intitle: "+deleteBadCharacters(song.name)
    # print("Searching Youtube for "+song.youtubeSearch)
    youtubeVideos = []
    while len(youtubeVideos) == 0:
        s = Search(song.youtubeSearch)
        i=0
        for r in s.results:
            # prGreen(f'Found {i+1} of {len(s.results)} results {round(100*(i+1) / len(s.results),2)}%')
            thisYoutubeSong = YoutubeSong(song,r)
            # print("debug")
            youtubeVideos.append(thisYoutubeSong)
            i+=1
        if len(youtubeVideos) == 0:
            song.youtubeSearch = trackArtists+" - "+deleteBadCharacters(song.name)
    return youtubeVideos
            
def getBestVideo(song: Song) -> str:
    song.bestMatch = None
    song.youtubeSongs = get_videos(song)
    difference = 0
    possibleSongList: List[YoutubeSong] =[]
    oneT=10**12
    while song.bestMatch is None:
        # print(song.bestMatch)
        for i,currentYoutubeVideo in enumerate(song.youtubeSongs):
            # print(f'Finding Best Video {i} of {len(song.youtubeSongs)} {100*i/len(song.youtubeSongs)}%                        ')
            # print(currentYoutubeVideo)
            currentYoutubeVideo.weight = currentYoutubeVideo.views            
            timediff = abs(int(currentYoutubeVideo.song.duration)-int(currentYoutubeVideo.length))            
            currentYoutubeVideo.notWithinTimeLimit = timediff > difference+(int(currentYoutubeVideo.song.duration)*0.05)
            currentYoutubeVideo.badTitle = not currentYoutubeVideo.isNotBad()
            currentYoutubeVideo.nameInTitle = cleanTrackName(deleteBadCharacters(currentYoutubeVideo.song.name)) in cleanTrackName(deleteBadCharacters(currentYoutubeVideo.title))
            currentYoutubeVideo.goodNameInTitle = currentYoutubeVideo.isVeryGood()
            currentYoutubeVideo.closeToTime = timediff<=difference
            if (currentYoutubeVideo.notWithinTimeLimit or currentYoutubeVideo.badTitle): continue
                
            if currentYoutubeVideo.nameInTitle: currentYoutubeVideo.weight += 3*oneT
            if currentYoutubeVideo.goodNameInTitle: currentYoutubeVideo.weight += 2*oneT
            if currentYoutubeVideo.closeToTime: currentYoutubeVideo.weight += 1*oneT 
            possibleSongList.append(currentYoutubeVideo)
        
        if (len(possibleSongList)!=0):
            possibleSongList.sort(key=lambda x: x.weight, reverse=True)
            song.bestMatch = possibleSongList[0]
            
            # for i in possibleSongList:
            #     print("HELLO",i.weight)
            saveToDebug(song)
            return song.bestMatch.youtubeLink
        # prRed(f'No suitable video found for {currentYoutubeVideo.song.name} within {difference} ms of the origninal',end='\r')
        difference+=1000

def saveToDebug(song: Song):
    print("saving to debug - "+song.list_name.rstrip()+"\\("+str(song.list_position)+") - "+removePunctuation(song.name)+".json")
    json_object = jsonpickle.encode(song)
    folder = "C:\\Users\\Owner\\Desktop\\spotify-downloader\\debug\\"+song.list_name.rstrip()
    if not os.path.exists(folder):
        os.makedirs(folder)
    # with open("C:\\Users\\Owner\\Desktop\\spotify-downloader\\debug\\"+song.list_name+"\\"+str(addZeros(len([entry for entry in os.listdir(folder) if os.path.isfile(os.path.join(folder, entry))])+1))+" - "+removePunctuation(song.name)+".json", "w") as outfile:
    with open(folder+"\\("+str(song.list_position)+") - "+removePunctuation(song.name)+".json", "w") as outfile:
        outfile.write(json.dumps(json.loads(json_object), indent=4))
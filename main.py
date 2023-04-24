import math
import re
import subprocess
import yt_dlp
import urllib.request
from spotdl.utils import spotify
from stdUtil import prLightPurple, CLIENT_ID, CLIENT_SECRET, getImage, getzeros, prCyan, prGreen, prPurple, PLAYLIST_FILE_NAME, printBar, removePunctuation ,validateFiles
import os
from os import walk
from spotipy.oauth2 import SpotifyClientCredentials
from sclib import SoundcloudAPI, Track, Playlist


def run():
    file = open(PLAYLIST_FILE_NAME,'r')
    validateFiles()
    for currentPlaylist in file.readlines():
        
        if "spotify" in currentPlaylist:
            search = re.search(r'(?<=https:\/\/open\.spotify\.com\/)[^\/]+',currentPlaylist)
            type2 = "saved" if search is None else search.group(0)
            # name = re.sub("^[^\s]+", "", currentPlaylist).strip()
            link = re.sub(" .*", "", currentPlaylist).strip()
            name = getImage(link,type2)
            prPurple(f"STARTING {type2}: {name}")
            # subprocess.Popen([ "python" ,"-m" ,'spotdl', link])
            subprocess.run([ "python" ,"-m" ,'spotdl', link])
            prCyan(f"{type2} COMPLETE : {name}")
        elif "soundcloud" in currentPlaylist.lower():
            api = SoundcloudAPI()
            link = re.sub(" .*", "", currentPlaylist).strip()
            playlist = api.resolve(link)
            type2 = "SoundCloud playlist"
            prPurple(f"STARTING {type2}: {playlist.title}")
            prGreen(f"Processing query: {link}")
            prGreen(f"Found {playlist.track_count} songs in {playlist.title} ({type2})")
            # search = re.search(r"/([^/ ]+)[^/]*$",currentPlaylist)
            # name =search.group(1)
            dir_path = r'D:\\Songs4\\.icons'
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            dir_path2 = f'D:\\Songs4\\{playlist.title}'
            if not os.path.exists(dir_path2):
                os.makedirs(dir_path2)
            # playlisturl = f'{dir_path}\\{playlist.title}.jpg'
            # print(playlisturl)
            # print(playlist.artwork_url)
            # urllib.request.urlretrieve(playlist.artwork_url, dir_path+"\\\\"+playlist.title+".jpg")
            
            assert type(playlist) is Playlist
            for x,track in enumerate(playlist.tracks,start=1):
                printBar(x,playlist.track_count,playlist.title,printEnd="\r")
                filename = f'D:\\Songs4\\{playlist.title}\\({getzeros(x,playlist.track_count)}) {removePunctuation(track.artist)} - {removePunctuation(track.title)}.mp3'
                if not os.path.isfile(filename):
                    with open(filename, 'wb+') as file:
                        track.write_mp3_to(file)
                    stri = f'Downloaded "{track.artist} - {track.title}": {track.permalink_url}'
                else:
                    stri = f'Skipping "{track.artist} - {track.title}" (file already exists)'
                
                prGreen(stri+ (os.get_terminal_size().columns - len(stri))*" ")
            prCyan(f"{type2} COMPLETE: {playlist.title}")
        elif "youtube" in currentPlaylist.lower():
            link = re.sub(" .*", "", currentPlaylist).strip()
            playlist = Playlist(link)
            URLS = [video_url for video_url in playlist]
            print(URLS)
            time.sleep(200)
            URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

            class MyLogger:
                def debug(self, msg):
                    # For compatibility with youtube-dl, both debug and info are passed into debug
                    # You can distinguish them by the prefix '[debug] '
                    if msg.startswith('[debug] '):
                        pass
                    else:
                        self.info(msg)

                def info(self, msg):
                    pass

                def warning(self, msg):
                    pass

                def error(self, msg):
                    print(msg)


            # ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
            def my_hook(d):
                if d['status'] == 'finished':
                    print('Done downloading, now post-processing ...')


            ydl_opts = {
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(URLS)
        pass
    prLightPurple("DONE ALL PLAYLISTS")
    
if __name__ == "__main__":
    run()
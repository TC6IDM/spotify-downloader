import math
import re
import subprocess
import time
from spotdl import console_entry_point
import yt_dlp
import urllib.request
from spotdl.utils import spotify
from stdUtil import COOKIE_FILE, USERNAME, deleteBadCharacters, prLightPurple, CLIENT_ID, CLIENT_SECRET, getImage, getzeros, prCyan, prGreen, prPurple, PLAYLIST_FILE_NAME, prYellow, printBar, removePunctuation ,validateFiles
import os
from os import walk
from spotipy.oauth2 import SpotifyClientCredentials
from sclib import SoundcloudAPI, Track, Playlist
from pytube import Playlist as YoutubePlaylist
import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotdl.types import artist
from spotdl.utils.spotify import SpotifyClient
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
                    
def run():
    namespace = argparse.Namespace(
        operation='download',
        query=['https://open.spotify.com/playlist/1RSAC3IJyyZh1YskiyUfl3?si=7b9879325daf4529'],
        audio_providers=None,
        lyrics_providers=None,
        config=False,
        search_query=None,
        filter_results=None,
        user_auth=None,
        client_id=None,
        client_secret=None,
        auth_token=None,
        cache_path=None,
        no_cache=None,
        max_retries=None,
        headless=None,
        ffmpeg=None,
        threads=None,
        bitrate=None,
        ffmpeg_args=None,
        format=None,
        save_file=None,
        preload=None,
        output=None,
        m3u=None,
        cookie_file=None,
        overwrite=None,
        restrict=None,
        print_errors=None,
        sponsor_block=None,
        archive=None,
        playlist_numbering=None,
        scan_for_songs=None,
        fetch_albums=None,
        id3_separator=None,
        ytm_data=None,
        add_unavailable=None,
        generate_lrc=None,
        force_update_metadata=None,
        host=None,
        port=None,
        keep_alive=None,
        allowed_origins=None,
        web_use_output_dir=None,
        keep_sessions=None,
        log_level=None,
        simple_tui=None,
        download_ffmpeg=False,
        generate_config=False,
        check_for_updates=False,
        profile=False
    )
    file = open(PLAYLIST_FILE_NAME,'r')
    # validateFiles()
    for currentPlaylist in file.readlines():
        if (currentPlaylist.startswith("/")): continue
        if "spotify" in currentPlaylist.lower():
            client_credentials_manager = SpotifyClientCredentials(
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET
            )
            # create spotify session object
            session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            search = re.search(r'(?<=https:\/\/open\.spotify\.com\/)[^\/]+',currentPlaylist)
            type2 = "saved" if search is None else search.group(0)
            link = re.sub(" .*", "", currentPlaylist).strip()
            # print(link)
            playlistLength = 10**12
            # if type2 == "playlist": playlistLength = session.user_playlist(USERNAME,link)['tracks']['total']
            # elif type2 == "album": playlistLength = session.album(link)['tracks']['total']
            # elif type2 == "artist":
            #     playlistLength = 10**12
                # results = session.artist_albums(link, album_type='album')
                # albums = results['items']
                # while results['next']:
                #     results = session.next(results)
                #     albums.extend(results['items'])
                # for album in albums:
                #     playlistLength+= session.album(album["external_urls"]["spotify"])['tracks']['total']
                # print(playlistLength)
                # time.sleep(3)
            name = getImage(link,type2)
            prPurple(f"STARTING {type2}: {name}")
            # print(str(playlistLength)+" "+ str(len(os.listdir(r"D:\\Songs4\\"+name))))
            # if playlistLength == len(os.listdir(r"D:\\Songs4\\"+name)): prYellow(f"SKIPPING {type2}: {name}")
            # while playlistLength > len(os.listdir(r"D:\\Songs4\\"+name)):
            # while True:
                # with open(r"C:\\Users\\Owner\\Desktop\\spotify-downloader\\newFiles.txt", 'r') as fp:
                #     startLen = len(fp.readlines())
                
                # name = re.sub("^[^\s]+", "", currentPlaylist).strip()
                
                
                
                # console_entry_point(namespace)
                # subprocess.Popen([ "python" ,"-m" ,'spotdl', link])
            subprocess.run([ "python" ,"-m" ,'spotdl', link])
            prCyan(f"{type2} COMPLETE: {name}")
                # with open(r"C:\\Users\\Owner\\Desktop\\spotify-downloader\\newFiles.txt", 'r') as fp:
                #     endLen = len(fp.readlines())
                # if endLen == startLen:
                #     print("No new files")
                #     break
                # else:
                #     time.sleep(5)
                #     prCyan(f"{type2} RESTARTING : {name}")
                # if type2 == "artist": break
                # break
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
                    file = open('C:\\Users\\Owner\\Desktop\\spotify-downloader\\newFiles.txt', 'a')
                    file.write(playlist.title+"\\"+str(x)+" "+deleteBadCharacters(track.title)+"\n")
                    file.close()
                else:
                    stri = f'Skipping "{track.artist} - {track.title}" (file already exists)'
                
                prGreen(stri+ (os.get_terminal_size().columns - len(stri))*" ")
            prCyan(f"{type2} COMPLETE: {playlist.title}")        
        # elif "youtube" in currentPlaylist.lower(): #WIP
        #     link = re.sub(" .*", "", currentPlaylist).strip()
        #     print(link)
        #     playlist = YoutubePlaylist(link)
        #     URLS = [video_url for video_url in playlist]
        #     # print(URLS)
        #     dir_path2 = f'D:\\Songs4\\{playlist.title}\\'
        #     # time.sleep(200)
        #     ydl_opts = {
        #     'format': 'mp3/bestaudio/best',
        #     'postprocessors': [{
        #         'key': 'FFmpegExtractAudio',
        #         'preferredcodec': 'mp3',
        #         'preferredquality': '320',#highest quality
        #     },{
        #         'key': 'FFmpegMetadata',
        #         'add_metadata': True,
        #     }],
        #     'ignoreerrors': True, #ignore errors
        #     'outtmpl': dir_path2+'(%(video_autonumber)s) %(uploader)s - %(title)s.%(ext)s', #save songs here .%(ext)s
        #     # 'outtmpl': dir_path2+"("+getzeros(int('%(video_autonumber)s'),int('%(playlist_count)s'))+') '+ removePunctuation("%(uploader)s")+ ' - ' +removePunctuation("%(title)s") +'.%(ext)s', #save songs here .%(ext)s
        #     'logger': MyLogger(),
        #     'progress_hooks': [my_hook],
        #     'cookiefile': COOKIE_FILE, #cookies for downloading age restricted videos
        #     }

        #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #         ydl.download(URLS)
        # pass
    prLightPurple("DONE ALL PLAYLISTS")
    
if __name__ == "__main__":
    while True:
        run()
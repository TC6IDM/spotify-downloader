import math
import re
import subprocess
from stdUtil import prPurple, PLAYLIST_FILE_NAME,validateFiles
import os
from os import walk

def run():
    file = open(PLAYLIST_FILE_NAME,'r')
    
    # folder path
    dir_path = r'D:\\Songs4\\'

    # list to store files name
    res = []
    for (dir_path, dir_names, file_names) in walk(dir_path):
        res.extend(dir_names)
    res2 = []
    dir_path = 'D:\\Songs4\\'
    for subfolder in res:
        for path in os.listdir(dir_path+subfolder):
            res2.append(dir_path+subfolder+"\\"+path)
    
    validateFiles(res2)
    for currentPlaylist in file.readlines():
        search = re.search(r'(?<=https:\/\/open\.spotify\.com\/)[^\/]+',currentPlaylist)
        type = "saved" if search is None else search.group(0)
        name = re.sub("^[^\s]+", "", currentPlaylist).strip()
        link = re.sub(" .*", "", currentPlaylist).strip()
        prPurple(f"STARTING {type}: {name}")
        # subprocess.Popen([ "python" ,"-m" ,'spotdl', link])
        subprocess.run([ "python" ,"-m" ,'spotdl', link])
        pass
    prPurple("DONE ALL PLAYLISTS")
    
if __name__ == "__main__":
    run()
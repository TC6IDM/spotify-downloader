import re
import subprocess
from stdUtil import prPurple, PLAYLIST_FILE_NAME
def run():
    file = open(PLAYLIST_FILE_NAME,'r')
    for currentPlaylist in file.readlines():
        search = re.search(r'(?<=https:\/\/open\.spotify\.com\/)[^\/]+',currentPlaylist)
        type = "saved" if search is None else search.group(0)
        name = re.sub("^[^\s]+", "", currentPlaylist).strip()
        link = re.sub(" .*", "", currentPlaylist).strip()
        prPurple(f"STARTING {type}: {name}")
        subprocess.run([ "python" ,"-m" ,'spotdl', link])
        pass
    prPurple("DONE ALL PLAYLISTS")
    
if __name__ == "__main__":
    run()
import json
import jsonpickle
from stdUtil import deleteBadCharacters
from spotdl.types.song import Song
class YoutubeSong:   
    def __init__(self,song: Song,youtubeVideo):
        # jsondata = jsonpickle.encode(youtubeVideo)
        # with open(f"123123213312321213213123123123tt.json", "w") as outfile:
        #     outfile.write(json.dumps(json.loads(jsondata), indent=4))
        # print(youtubeVideo.video_id)
        self.id = youtubeVideo.video_id
        # print(youtubeVideo.watch_url)
        self.youtubeLink=youtubeVideo.watch_url
        # print(youtubeVideo.length)
        self.length = extract_ms(youtubeVideo.length)
        # print(youtubeVideo.title)
        self.title = youtubeVideo.title
        # print( youtubeVideo.views)
        self.views = youtubeVideo.views
        # print( self.views)
        self.weight = self.views
        self.notWithinTimeLimit = False
        self.badTitle = False
        self.nameInTitle = False
        self.goodNameInTitle = False
        self.closeToTime = False
        self.song = song
    
    def isNotBad(self):
        trackArtistsPlain = [deleteBadCharacters(artist) for artist in self.song.artists]
        trackArtists = "/".join(trackArtistsPlain)
        blacklistDirty = ["clean"]
        blacklist = ["instrumental",
                 "8d",
                 "1 hour",
                 "full album",
                 "alternative",
                 "sped up",
                 "acapella",
                 "vocals only",
                 "extended",
                 "slowed",
                 "reverb",
                 "bass boosted",
                 "dance challenge"]
        if self.song.explicit: 
            blacklist = blacklist + blacklistDirty
        for i in blacklist:
            if (i in self.title.lower()) and (i not in trackArtists.lower()) and (i not in self.song.name.lower()): return False #if word is in the title, it must be in the artist or song name
        return True

    def isVeryGood(self):
        blacklistDirty = ["uncensored",
                    "explicit",]
        blacklist = ["official audio",
                    "high quality",
                    "hq",
                    "official visualizer",
                    "visualizer",
                    "lyrics",
                    "(audio)"]
        if self.song.explicit: 
            blacklist = blacklist + blacklistDirty
        
        for i in blacklist:
            if (i in self.title.lower()): return True #
        return False

def extract_ms(time_str):
    if not isinstance(time_str, str):
        return time_str
    # Split the string by comma and space
    parts = time_str.split(', ')
    # Extract hours, minutes, and seconds
    try:
        total_seconds = 0
        for part in parts:
            # Check if it's hours, minutes, or seconds
            if 'hour' in part:
                total_seconds += int(part.split()[0]) * 3600
            elif 'minute' in part:
                total_seconds += int(part.split()[0]) * 60
            elif 'second' in part:
                total_seconds += int(part.split()[0])
        return total_seconds * 1000
    except ValueError:
        return "Invalid input"
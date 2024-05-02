import yt_dlp
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
        
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')     
        
URLS = ['https://www.youtube.com/watch?v=tia-BfapcaI&ab_channel=YZY','https://www.youtube.com/watch?v=uDkGe4BsQt0&ab_channel=YZY']
ydl_opts = {
'format': 'mp4/bestaudio/best',
# 'postprocessors': [{
#     'key': 'FFmpegExtractAudio',
#     'preferredcodec': 'mp4',
#     'preferredquality': '320',#highest quality
# },{
#     'key': 'FFmpegMetadata',
#     'add_metadata': True,
# }],
'ignoreerrors': True, #ignore errors
'outtmpl': 'C:\\Users\\Owner\\Desktop\\ye\\(%(video_autonumber)s) %(uploader)s - %(title)s.%(ext)s', #save songs here .%(ext)s
# 'outtmpl': dir_path2+"("+getzeros(int('%(video_autonumber)s'),int('%(playlist_count)s'))+') '+ removePunctuation("%(uploader)s")+ ' - ' +removePunctuation("%(title)s") +'.%(ext)s', #save songs here .%(ext)s
'logger': MyLogger(),
'progress_hooks': [my_hook],
# 'cookiefile': COOKIE_FILE, #cookies for downloading age restricted videos
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)
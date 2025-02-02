from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL

class getVideosThread(QThread):
    finishedSearch = Signal(list)

    def __init__(self, query: str, amount: int = 12):
        super().__init__()
        self.query = query
        self.amount = amount

    def run(self):
        ydl_opts = {'quiet': True, 'extract_flat': True, 'noplaylist': True}
        with YoutubeDL(ydl_opts) as ytdl:
            info: dict = ytdl.extract_info(f'ytsearch{self.amount}:{self.query}', download=False)  # type: ignore

        res = []
        if 'entries' in info:
            for video in info['entries']:
                if video['duration']:  # evita lives
                    res.append({
                        'title': video['title'],
                        'duration': video['duration'],
                        'channel': video['channel'],
                        'thumbnail': video['thumbnails'][0]['url'],
                        'link': video['url']
                    })

        self.finishedSearch.emit(res)
        self.quit()


class DownloadVideoThread(QThread):
    finishedDownload = Signal()
    error = Signal(str)
    progress = Signal(int)

    def __init__(self, url: str, path: str, quality: str, formatType: str, audioOnly: bool = False):
        super().__init__()
        self.url = url
        self.path = path
        self.quality = quality
        self.formatType = formatType
        self.audioOnly = audioOnly

    def run(self):
        try:
            ydl_opts = {
                'quiet': True,
                'format': f'bestvideo[ext=mp4][vcodec^=avc1][height<={self.quality}]+bestaudio[ext=m4a]/best',
                'outtmpl': f'{self.path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'merge_output_format': self.formatType,  # mp4/mp3
            }
            if self.audioOnly:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': self.quality
                }]

            with YoutubeDL(ydl_opts) as ytdl:
                ytdl.download([self.url])

            self.finishedDownload.emit()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.quit()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes', d.get('total_bytes_estimate', None))
            downloaded = d['downloaded_bytes']
            if total:
                self.progress.emit(int(downloaded / total * 100))


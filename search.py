from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL

class getVideosThread(QThread):
    finishedSearch = Signal(list)

    def __init__(self, query: str):
        super().__init__()
        self.query = query
        self.amount = 16  # hard coded por enquanto, depois obter quantia das configurações

    def run(self):
        ydl_opts = {'quiet': True, 'extract_flat': True, 'noplaylist': True}
        with YoutubeDL(ydl_opts) as ytdl:
            info: dict = ytdl.extract_info(f'ytsearch16:{self.query}', download=False)  # type: ignore

        res = []
        if 'entries' in info:
            for video in info['entries']:
                res.append({
                    'title': video['title'],
                    'duration': video['duration'],
                    'channel': video['channel'],
                    'thumbnail': video['thumbnails'][0]['url'],
                    'link': video['url']
                })

        self.finishedSearch.emit(res)
        self.quit()

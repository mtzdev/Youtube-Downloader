from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, GeoRestrictedError, UnavailableVideoError
from utils import Translator

class getVideosThread(QThread):
    finishedSearch = Signal(list)

    def __init__(self, query: str, amount: int = 12):
        super().__init__()
        self.query = query
        self.amount = amount

    def run(self):
        ydl_opts = {'quiet': True, 'extract_flat': True, 'noplaylist': True}
        try:
            with YoutubeDL(ydl_opts) as ytdl:
                info: dict = ytdl.extract_info(f'ytsearch{self.amount}:{self.query}', download=False)  # type: ignore

            res = []
            if 'entries' in info:
                for video in info['entries']:
                    if video['ie_key'] == 'Youtube':  # fix: evita infos que não são videos
                        if video['duration']:  # evita lives
                            res.append({
                                'title': video['title'],
                                'duration': video['duration'],
                                'channel': video['channel'],
                                'thumbnail': video['thumbnails'][0]['url'],
                                'link': video['url']
                            })

            self.finishedSearch.emit(res)
        except Exception:
            self.finishedSearch.emit([])
        finally:
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

        self.i18n = Translator()

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

        except GeoRestrictedError:
            self.error.emit(self.i18n.get('geo_restricted_error'))
        except UnavailableVideoError:
            self.error.emit(self.i18n.get('unavailable_video_error'))
        except DownloadError:
            self.error.emit(self.i18n.get('download_generic_error'))
        except Exception as e:
            self.error.emit(f'{self.i18n.get("unknown_error")} {e}')
        finally:
            self.quit()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes', d.get('total_bytes_estimate', None))
            downloaded = d['downloaded_bytes']
            if total:
                self.progress.emit(int(downloaded / total * 100))


class getVideoFromURLThread(QThread):
    finishedSearch = Signal(list)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        ydl_opts = {
            'quiet': True,
            'extract_flat': False,
            'noplaylist': True
        }

        i18n = Translator()

        try:
            with YoutubeDL(ydl_opts) as ytdl:
                info = ytdl.extract_info(self.url, download=False)

                if not info or not info.get('duration'):
                    self.finishedSearch.emit([])
                    return

                result = [{
                    'title': info.get('title', i18n.get('no_title')),
                    'duration': info.get('duration', 0),
                    'channel': info.get('uploader', info.get('channel', i18n.get('unknown_channel'))),
                    'thumbnail': info.get('thumbnail', '') if not info.get('thumbnails') else info['thumbnails'][0]['url'],
                    'link': info.get('webpage_url', self.url)
                }]

                self.finishedSearch.emit(result)

        except Exception:
            self.finishedSearch.emit([])
        finally:
            self.quit()


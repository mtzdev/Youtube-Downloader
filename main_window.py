from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidgetItem, QMessageBox
from PySide6.QtGui import QIcon, QPixmap, QMovie
from PySide6.QtCore import Qt, QSize, QUrl, QByteArray
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from configurations import MainSettings, DownloadSettings
from search import getVideosThread, getVideoFromURLThread
import re
from utils import get_resource, Translator, CURRENT_VERSION

from ui.MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Youtube Downloader")
        self.setFixedSize(self.width(), self.height())
        self.networkManager = QNetworkAccessManager()
        self.statusbar.showMessage(f"Version {CURRENT_VERSION} - by mtzdev")
        self.i18n = Translator()

        self.loadingGif = QMovie(get_resource("data/loading.gif"))
        self.loadingLabel.setMovie(self.loadingGif)
        self.listWidget.itemClicked.connect(self.listWidget_itemClicked)

        self.searchButton = self.searchBar.addAction(QIcon(get_resource("data/search_dark.svg")), self.searchBar.ActionPosition.LeadingPosition)
        self.searchBar.setStyleSheet("border-radius: 6px; font-size: 15px")
        self.searchButton.triggered.connect(self.startSearch)
        self.searchBar.returnPressed.connect(self.startSearch)

        self.clearButton = self.searchBar.addAction(QIcon(get_resource("data/x.png")), self.searchBar.ActionPosition.TrailingPosition)
        self.clearButton.triggered.connect(lambda: self.searchBar.clear())
        self.clearButton.setVisible(False)
        self.searchBar.textChanged.connect(lambda: self.clearButton.setVisible(bool(self.searchBar.text())))

        self.configs = MainSettings(self.i18n)
        self.configButton.setIcon(QIcon(get_resource("data/config_dark.svg")))
        self.configButton.setIconSize(QSize(22, 22))
        self.configButton.setToolTip("Configurações")
        self.configButton.clicked.connect(self.configs.showConfigs)

        self.configs.themeChanged.connect(self.changeIconTheme)

    def changeIconTheme(self, theme):
        if theme == 'light':
            self.searchButton.setIcon(QIcon(get_resource("data/search_light.svg")))
            self.configButton.setIcon(QIcon(get_resource("data/config_light.svg")))
            self.searchBar.setStyleSheet("border-color: #898989; border-radius: 6px; font-size: 15px; color: #000000")
            self.configButton.setStyleSheet("border-color: #898989;")
            self.listWidget.setStyleSheet("border-color: #898989")

        if theme == 'dark':
            self.searchButton.setIcon(QIcon(get_resource("data/search_dark.svg")))
            self.configButton.setIcon(QIcon(get_resource("data/config_dark.svg")))
            self.searchBar.setStyleSheet("border-radius: 6px; font-size: 15px")
            self.configButton.setStyleSheet("")
            self.listWidget.setStyleSheet("")

    def startSearch(self):
        query = self.searchBar.text()
        if query.strip() == '':
            return

        self.searchBar.setDisabled(True)
        self.listWidget.clear()
        self.loadingLabel.show()
        self.loadingGif.start()

        if bool(re.match(r"^(https?:\/\/)?(www\.)?(youtu\.be\/|youtube\.com\/)", query)):  # links do yt
            match = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/|shorts/|live/))([^?&]+)", query)
            if match:
                query = match.group(1)
                self.search_thread = getVideosThread(query, self.configs.searchLimit.value())
            else:
                QMessageBox.information(self, self.i18n.get("link_not_supported"), self.i18n.get("link_not_supported_desc"), QMessageBox.Ok)
                return

        elif bool(re.match(r"^(https?:\/\/)[^\s/$.?#].[^\s]*$", query)):  # links em geral
            self.search_thread = getVideoFromURLThread(query)

        else:  # pesquisa
            self.search_thread = getVideosThread(query, self.configs.searchLimit.value())


        self.search_thread.finishedSearch.connect(self.processVideoResults)
        self.search_thread.finishedSearch.connect(self.unlockSearch)
        self.search_thread.finishedSearch.connect(self.search_thread.deleteLater)
        self.search_thread.start()

    def unlockSearch(self):
        self.searchBar.setDisabled(False)
        self.loadingLabel.setHidden(True)
        self.loadingGif.stop()

    def processVideoResults(self, results):
        if not results:
            QMessageBox.information(self, self.i18n.get("no_results"), self.i18n.get("no_results_desc"), QMessageBox.Ok)
            return

        for video in results:
            self.add_video_to_list(video['title'], video['channel'], video['duration'], video['thumbnail'], video['link'])

    def load_thumbnail(self, url, label, w: int, h: int):
        request = QNetworkRequest(QUrl(url))
        reply = self.networkManager.get(request)

        def thumbnail_loaded(reply: QNetworkReply):
            if reply.error() != QNetworkReply.NetworkError.NoError:
                return None

            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(data))
            scaled_pixmap = pixmap.scaled(w, h)
            label.setPixmap(scaled_pixmap)
        reply.finished.connect(lambda: thumbnail_loaded(reply))

    def add_video_to_list(self, title, channel, duration, thumbnail, url):
        item = QWidget(self)
        itemLayout = QHBoxLayout(item)

        thumbLabel = QLabel()
        thumbLabel.setStyleSheet('border: 0px')
        self.load_thumbnail(thumbnail, thumbLabel, 120, 65)
        thumbLabel.setFixedSize(120, 65)
        itemLayout.addWidget(thumbLabel)

        infosLayout = QVBoxLayout()
        infosLayout.setContentsMargins(0, 0, 0, 0)
        infosLayout.setSpacing(2)

        titleLabel = QLabel(title)
        titleLabel.setStyleSheet('font-size: 14px; font-weight: bold; border: 0px;')

        channelLabel = QLabel(f'{self.i18n.get("channel")}: {channel}')
        channelLabel.setStyleSheet('font-size: 12px; color: gray; border: 0px;')

        duration = int(duration)
        if duration >= 3600:
            durationLabel = QLabel(f'{self.i18n.get("duration")}: {duration // 3600:02d}:{(duration % 3600) // 60:02d}:{duration % 60:02d}')
        else:
            durationLabel = QLabel(f'{self.i18n.get("duration")}: {duration // 60:02d}:{duration % 60:02d}')

        durationLabel.setStyleSheet('font-size: 12px; color: gray; border: 0px;')

        infosLayout.addWidget(titleLabel)
        infosLayout.addWidget(channelLabel)
        infosLayout.addWidget(durationLabel)
        itemLayout.addLayout(infosLayout)

        item.setProperty('infos', (title, channel, duration, thumbnail, url))

        item.setCursor(Qt.CursorShape.PointingHandCursor)
        item.setStyleSheet("QWidget:hover { border: 2px solid #B0B0B0; border-radius: 5px; }")

        listItem = QListWidgetItem()
        listItem.setSizeHint(item.sizeHint())
        self.listWidget.addItem(listItem)
        self.listWidget.setItemWidget(listItem, item)

    def listWidget_itemClicked(self, item: QListWidgetItem):
        video = self.listWidget.itemWidget(item).property('infos')

        download = DownloadSettings(video, self.configs, self.i18n)
        self.load_thumbnail(video[3], download.thumbLabel, 90, 54)
        download.showConfigs()
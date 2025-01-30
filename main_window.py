from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidgetItem
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QUrl, QByteArray
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from configurations import MainSettings
from search import getVideosThread
import re

from ui.MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Youtube Downloader")
        self.setFixedSize(self.width(), self.height())
        self.networkManager = QNetworkAccessManager()

        self.searchButton = self.searchBar.addAction(QIcon("data/search_dark.svg"), self.searchBar.ActionPosition.LeadingPosition)
        self.searchBar.setStyleSheet("border-radius: 6px; font-size: 15px")
        self.searchBar.returnPressed.connect(self.startSearch)

        self.configs = MainSettings()
        self.configButton.setIcon(QIcon("data/config_dark.svg"))
        self.configButton.setIconSize(QSize(22, 22))
        self.configButton.setToolTip("Configurações")
        self.configButton.clicked.connect(self.configs.showConfigs)

        self.configs.themeChanged.connect(self.changeIconTheme)

    def changeIconTheme(self, theme):
        if theme == 'Claro':
            self.searchButton.setIcon(QIcon("data/search_light.svg"))
            self.configButton.setIcon(QIcon("data/config_light.svg"))
            self.searchBar.setStyleSheet("border-color: #898989; border-radius: 6px; font-size: 15px; color: #000000")
            self.configButton.setStyleSheet("border-color: #898989;")
            self.listWidget.setStyleSheet("border-color: #898989")

        if theme == 'Escuro':
            self.searchButton.setIcon(QIcon("data/search_dark.svg"))
            self.configButton.setIcon(QIcon("data/config_dark.svg"))
            self.searchBar.setStyleSheet("border-radius: 6px; font-size: 15px")
            self.configButton.setStyleSheet("")
            self.listWidget.setStyleSheet("")

    def startSearch(self):
        query = self.searchBar.text()
        if query == '':
            return

        self.searchBar.setDisabled(True)

        if re.match(r'^https://www.youtube.com/watch\?v=[a-zA-Z0-9_-]{11}$', query):
            # TODO: baixar video direto caso seja um link
            return

        self.listWidget.clear()

        self.search_thread = getVideosThread(query)
        self.search_thread.finishedSearch.connect(self.processVideoResults)
        self.search_thread.finishedSearch.connect(self.unlockSearch)
        self.search_thread.finishedSearch.connect(self.search_thread.deleteLater)
        self.search_thread.start()

    def unlockSearch(self):
        self.searchBar.setDisabled(False)

    def processVideoResults(self, results):
        for video in results:
            self.add_video_to_list(video['title'], video['channel'], video['duration'], video['thumbnail'], video['link'])

    def load_thumbnail(self, url, label):
        request = QNetworkRequest(QUrl(url))
        reply = self.networkManager.get(request)

        def thumbnail_loaded(reply: QNetworkReply):
            if reply.error() != QNetworkReply.NetworkError.NoError:
                return

            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(data))
            label.setPixmap(pixmap.scaled(120, 65))
        reply.finished.connect(lambda: thumbnail_loaded(reply))

    def add_video_to_list(self, title, channel, duration, thumbnail, url):
        item = QWidget(self)
        itemLayout = QHBoxLayout(item)

        thumbLabel = QLabel()
        self.load_thumbnail(thumbnail, thumbLabel)
        thumbLabel.setFixedSize(120, 65)
        itemLayout.addWidget(thumbLabel)

        infosLayout = QVBoxLayout()
        infosLayout.setContentsMargins(0, 0, 0, 0)
        infosLayout.setSpacing(2)

        titleLabel = QLabel(title)
        titleLabel.setStyleSheet('font-size: 14px; font-weight: bold')

        channelLabel = QLabel(f'Canal: {channel}')
        channelLabel.setStyleSheet('font-size: 12px; color: gray')
        try:
            durationLabel = QLabel(f'Duração: {duration // 60:.0f}:{duration % 60:.0f}')  # TODO: formatar duração
        except TypeError:
            durationLabel = QLabel('Duração: -')

        durationLabel.setStyleSheet('font-size: 12px; color: gray')

        infosLayout.addWidget(titleLabel)
        infosLayout.addWidget(channelLabel)
        infosLayout.addWidget(durationLabel)
        itemLayout.addLayout(infosLayout)

        item.setProperty('url', url)

        listItem = QListWidgetItem()
        listItem.setSizeHint(item.sizeHint())
        self.listWidget.addItem(listItem)
        self.listWidget.setItemWidget(listItem, item)
        self.listWidget.itemClicked.connect(self.listWidget_itemClicked)

    def listWidget_itemClicked(self, item):
        ...

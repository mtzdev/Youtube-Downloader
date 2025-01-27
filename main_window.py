from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from configurations import MainSettings

from ui.MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Youtube Downloader")
        self.setFixedSize(self.width(), self.height())

        self.searchButton = self.searchBar.addAction(QIcon("data/search_dark.svg"), self.searchBar.ActionPosition.LeadingPosition)
        self.searchBar.setStyleSheet("border-radius: 6px; font-size: 15px")

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

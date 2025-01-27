from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from configurations import Configuration

from ui.MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(self.width(), self.height())

        searchButton = self.searchBar.addAction(QIcon("data/search.svg"), self.searchBar.ActionPosition.LeadingPosition)
        self.searchBar.setStyleSheet("border-radius: 6px; font-size: 15px")
        # searchButton.triggered.connect(lambda: print('realizando busca...')
        # self.searchBar.returnPressed.connect(lambda: print('realizando busca...'))

        self.configs = Configuration()
        self.configButton.setIcon(QIcon("data/config.svg"))
        self.configButton.setIconSize(QSize(22, 22))
        self.configButton.setToolTip("Configurações")
        self.configButton.clicked.connect(self.configs.showConfigs)

import requests
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from main_window import MainWindow
from utils import Settings, get_resource, Translator, CURRENT_VERSION
import qdarktheme
import sys
import webbrowser

GITHUB_URL = 'https://api.github.com/repos/mtzdev/Youtube-Downloader/releases/latest'

def main():
    app = QApplication([])
    window = MainWindow()

    config = Settings()
    config.setupSettings()

    check_for_updates(window)

    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation')

    app.setStyleSheet(qdarktheme.load_stylesheet(config.theme))
    if config.theme == 'light':  # mudar para light, pois por default ele já carrega dark
        window.changeIconTheme('light')

    window.setWindowIcon(QIcon(get_resource("data/logo.ico")))
    window.configs.themeChanged.connect(lambda theme: app.setStyleSheet(qdarktheme.load_stylesheet(theme)))

    window.show()
    app.exec()

def version_to_tuple(version):
    return tuple(map(int, version.lstrip('v').split('.')))

def check_for_updates(parent):
    try:
        response = requests.get(GITHUB_URL)
        if response.status_code == 200:
            latest_version = response.json()
            if version_to_tuple(latest_version['tag_name']) > version_to_tuple(CURRENT_VERSION):
                return update_available(parent, latest_version['html_url'])
    except Exception:
        pass

def update_available(parent, download_link):
    translate = Translator()
    msg = QMessageBox.question(parent, translate.get('update'), translate.get('update_desc'), QMessageBox.Yes | QMessageBox.No)
    if msg == QMessageBox.Yes:
        webbrowser.open(download_link)
        exit(0)

if __name__ == "__main__":
    main()
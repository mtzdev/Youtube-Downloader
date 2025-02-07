from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from main_window import MainWindow
from utils import Settings, get_resource
import qdarktheme
import sys

THEMES = {
    'Claro': 'light',
    'Escuro': 'dark'
}

def main():
    app = QApplication([])
    window = MainWindow()

    config = Settings()
    config.setupSettings()

    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation')

    app.setStyleSheet(qdarktheme.load_stylesheet(config.theme))
    if config.theme == 'light':  # mudar para light, pois por default ele já carrega dark
        window.changeIconTheme('Claro')

    window.setWindowIcon(QIcon(get_resource("data/logo.ico")))
    window.configs.themeChanged.connect(lambda theme: app.setStyleSheet(qdarktheme.load_stylesheet(THEMES[theme])))

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
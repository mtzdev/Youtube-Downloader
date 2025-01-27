from PySide6.QtWidgets import QApplication
from main_window import MainWindow
import qdarktheme

THEMES = {
    'Claro': 'light',
    'Escuro': 'dark'
}

def main():
    app = QApplication([])
    window = MainWindow()
    app.setStyleSheet(qdarktheme.load_stylesheet('dark'))

    window.configs.themeChanged.connect(lambda theme: app.setStyleSheet(qdarktheme.load_stylesheet(THEMES[theme])))

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from utils import Settings
import qdarktheme

THEMES = {
    'Claro': 'light',
    'Escuro': 'dark'
}

def main():
    app = QApplication([])
    window = MainWindow()

    config = Settings()
    config.setupSettings()

    app.setStyleSheet(qdarktheme.load_stylesheet(config.theme))
    if config.theme == 'light':  # mudar para light, pois por default ele já carrega dark
        window.changeIconTheme('Claro')

    window.configs.themeChanged.connect(lambda theme: app.setStyleSheet(qdarktheme.load_stylesheet(THEMES[theme])))

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
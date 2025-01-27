from PySide6.QtWidgets import QApplication
from main_window import MainWindow
import qdarktheme

def main():
    app = QApplication([])
    window = MainWindow()
    app.setStyleSheet(qdarktheme.load_stylesheet('dark'))

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
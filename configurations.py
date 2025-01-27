from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QComboBox, QPushButton
from PySide6.QtCore import Qt, QRect

class Configuration(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(340, 280)

        self.videoInfo = QFrame(self)
        self.videoInfo.setGeometry(QRect(10, 10, 321, 61))
        self.videoInfo.setFrameShape(QFrame.Shape.Box)


        self.fileFormatBox = QComboBox(self)
        self.fileFormatBox.addItem(".mp4")
        self.fileFormatBox.addItem(".mp3")
        self.fileFormatBox.setGeometry(QRect(20, 120, 141, 31))
        self.fileFormatBox.setStyleSheet(u"font: 16px \"Segoe UI\";\nborder-radius: 6px;")

        self.qualityBox = QComboBox(self)
        self.qualityBox.addItem("1080p")
        self.qualityBox.addItem("720p")
        self.qualityBox.addItem("480p")
        self.qualityBox.setGeometry(QRect(180, 120, 141, 31))
        self.qualityBox.setStyleSheet(u"font: 16px \"Segoe UI\";\nborder-radius: 6px;")

        self.pushButton = QPushButton(self)
        self.pushButton.setText("BAIXAR")
        self.pushButton.setGeometry(QRect(95, 190, 151, 41))
        self.pushButton.setStyleSheet(u"font:24px bold \"Segoe UI\";")


    def showConfigs(self):
        self.show()
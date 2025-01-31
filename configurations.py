from PySide6.QtWidgets import QWidget, QFrame, QComboBox, QPushButton, QLabel, QFileDialog, QMessageBox, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QRect, Signal, Slot
from pathlib import Path

class DownloadSettings(QWidget):
    def __init__(self, videoInfos: tuple):
        super().__init__()
        self.title = videoInfos[0]
        self.channel = videoInfos[1]
        self.duration = videoInfos[2]
        self.url = videoInfos[4]
        self.mp4Types = ["1080p", "720p", "480p", "360p"]
        self.mp3Types = ["320kbps", "256kbps", "192kbps", "128kbps"]

        self.setupUI()
        self.fileFormatBox.currentTextChanged.connect(lambda formatType: self.updateQualityBox(formatType))

    def setupUI(self):
        self.setWindowTitle("Configurações de Download")
        self.setFixedSize(360, 280)

        videoInfo = QFrame(self)
        videoInfo.setGeometry(QRect(5, 10, 350, 61))
        videoInfo.setFrameShape(QFrame.Shape.Box)

        frameLyt = QHBoxLayout(videoInfo)
        frameLyt.setContentsMargins(5, 5, 3, 5)
        self.thumbLabel = QLabel()
        self.thumbLabel.setGeometry(QRect(3, 3, 90, 54))
        frameLyt.addWidget(self.thumbLabel)

        infosLyt = QVBoxLayout()
        frameLyt.addLayout(infosLyt)

        title = QLabel(f'{self.title[:31]}...' if len(self.title) > 33 else self.title)
        title.setMinimumWidth(260)
        title.setToolTip(self.title)
        title.setStyleSheet("font: 14px")
        infosLyt.addWidget(title)

        if self.duration >= 3600:
            durationtxt = f'Duração: {self.duration // 3600:02d}:{(self.duration % 3600) // 60:02d}:{self.duration % 60:02d}'
        else:
            durationtxt = f'Duração: {self.duration // 60:02d}:{self.duration % 60:02d}'

        infos = QLabel(f"Canal: {self.channel} • Duração: {durationtxt}")
        infos.setContentsMargins(0, 0, 0, 5)
        infos.setStyleSheet("font: 12px; color: gray")
        infosLyt.addWidget(infos)

        self.fileFormatBox = QComboBox(self)
        self.fileFormatBox.addItem(".mp4 (Video)")
        self.fileFormatBox.addItem(".mp3 (Audio)")
        self.fileFormatBox.setGeometry(QRect(29, 120, 141, 31))
        self.fileFormatBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.fileFormatBox.setStyleSheet("font: 16px \"Segoe UI\";\nborder-radius: 6px;")

        self.qualityBox = QComboBox(self)
        self.qualityBox.addItems(self.mp4Types)
        self.qualityBox.setGeometry(QRect(190, 120, 141, 31))
        self.qualityBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.qualityBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.qualityBox.setStyleSheet("font: 16px \"Segoe UI\";\nborder-radius: 6px;")

        self.downloadButton = QPushButton(self)
        self.downloadButton.setText("BAIXAR")
        self.downloadButton.setGeometry(QRect(104, 190, 152, 41))
        self.downloadButton.setStyleSheet("font:24px bold \"Segoe UI\";")

    @Slot()
    def updateQualityBox(self, formatType: str):
        formats = {
            ".mp4 (Video)": self.mp4Types,
            ".mp3 (Audio)": self.mp3Types
        }
        self.qualityBox.clear()
        self.qualityBox.addItems(formats[formatType])

    def showConfigs(self):
        self.show()

class MainSettings(QWidget):
    themeChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.path = None

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Configurações")
        self.setFixedSize(229, 238)

        self.themeLabel = QLabel('Tema:', self)
        self.themeLabel.setGeometry(QRect(20, 30, 70, 32))
        self.themeLabel.setStyleSheet("font: 18pt \"Segoe UI\";")

        self.themeSelector = QComboBox(self)
        self.themeSelector.addItem("Claro")
        self.themeSelector.addItem("Escuro")
        self.themeSelector.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.themeSelector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.themeSelector.setCurrentText("Escuro")
        self.themeSelector.setGeometry(QRect(100, 30, 81, 30))
        self.themeSelector.setStyleSheet("font: 18px \"Segoe UI\"; border-radius: 6px")
        self.themeSelector.currentTextChanged.connect(self.themeChanged.emit)

        self.downloadPathLabel = QLabel("Local de Download:", self)  # TODO: implementar botão e logica para definir local de download
        self.downloadPathLabel.setGeometry(QRect(10, 80, 210, 31))
        self.downloadPathLabel.setStyleSheet("font: 17pt \"Segoe UI\";")

        self.downloadPathButton = QPushButton("Clique aqui para definir", self)
        self.downloadPathButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.downloadPathButton.setGeometry(QRect(18, 112, 194, 30))
        self.downloadPathButton.clicked.connect(self.selectPath)

        self.saveButton = QPushButton("Salvar modificações", self)
        self.saveButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.saveButton.setGeometry(QRect(15, 170, 198, 36))
        self.saveButton.setStyleSheet("font: 20px bold \"Segoe UI\"; border-radius: 10px;")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def showConfigs(self):
        self.show()

    def saveConfigs(self):
        self.close()
        # TODO: implementar salvar configs no db

    def selectPath(self):
        fileDialog = QFileDialog.getExistingDirectory(self, "Selecione o diretório de download")

        if fileDialog == "":
            return
        try:
            self.path = Path(fileDialog)
        except Exception:
            QMessageBox.critical(self, "Erro", "Ocorreu um erro ao selecionar o diretório de download.\nTente selecionar outra pasta.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return

        if len(str(self.path)) > 30:
            self.downloadPathButton.setText('...' + str(self.path)[-28:])
            self.downloadPathButton.setStyleSheet('text-align: right;')
        else:
            self.downloadPathButton.setText(str(self.path))
            self.downloadPathButton.setStyleSheet('text-align: auto;')
        self.downloadPathButton.setToolTip(str(self.path))
        return fileDialog

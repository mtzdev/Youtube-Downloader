from PySide6.QtWidgets import QWidget, QFrame, QComboBox, QPushButton, QLabel, QFileDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QProgressBar, QSpinBox
from PySide6.QtCore import Qt, QRect, Signal, Slot
from pathlib import Path
from search import DownloadVideoThread
from os import path
from utils import Settings

class DownloadSettings(QWidget):
    def __init__(self, videoInfos: tuple, mainConfigs):
        super().__init__()
        self.title = videoInfos[0]
        self.channel = videoInfos[1]
        self.duration = videoInfos[2]
        self.url = videoInfos[4]
        self.config = mainConfigs
        self.mp4Types = ["1080p", "720p", "480p", "360p", "240p"]
        self.mp3Types = ["320kbps", "256kbps", "192kbps", "128kbps", "96kbps"]

        self.setupUI()
        self.fileFormatBox.currentTextChanged.connect(lambda formatType: self.updateQualityBox(formatType))

    def setupUI(self):
        self.setWindowTitle("Configurações de Download")
        self.setFixedSize(360, 230)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

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

        title = QLabel(f'{self.title[:34]}...' if len(self.title) > 34 else self.title)
        title.setMinimumWidth(240)
        title.setToolTip(self.title)
        title.setStyleSheet("font: 14px")
        infosLyt.addWidget(title)

        if self.duration >= 3600:
            durationtxt = f'{self.duration // 3600:02d}:{(self.duration % 3600) // 60:02d}:{self.duration % 60:02d}'
        else:
            durationtxt = f'{self.duration // 60:02d}:{self.duration % 60:02d}'

        infos = QLabel(f"Canal: {self.channel} • Duração: {durationtxt}")
        infos.setContentsMargins(0, 0, 0, 5)
        infos.setStyleSheet("font: 12px; color: gray")
        infosLyt.addWidget(infos)

        self.fileFormatBox = QComboBox(self)
        self.fileFormatBox.addItem(".mp4 (Vídeo)")
        self.fileFormatBox.addItem(".mp3 (Áudio)")
        self.fileFormatBox.setGeometry(QRect(29, 90, 141, 31))
        self.fileFormatBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.fileFormatBox.setStyleSheet("font: 16px \"Segoe UI\";\nborder-radius: 6px;")

        self.qualityBox = QComboBox(self)
        self.qualityBox.addItems(self.mp4Types)
        self.qualityBox.setGeometry(QRect(190, 90, 141, 31))
        self.qualityBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.qualityBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.qualityBox.setStyleSheet("font: 16px \"Segoe UI\";\nborder-radius: 6px;")

        self.downloadButton = QPushButton(self)
        self.downloadButton.setText("BAIXAR")
        self.downloadButton.setGeometry(QRect(104, 145, 152, 41))
        self.downloadButton.setStyleSheet("font:24px bold \"Segoe UI\";")
        self.downloadButton.clicked.connect(self.downloadClicked)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(QRect(60, 210, 241, 25))
        self.progress.setValue(0)
        self.progress.setHidden(True)

        self.downloadPath = QPushButton('Pasta de Download: NÃO DEFINIDO! (clique aqui para definir)', self)
        if self.config.path is not None:
            self.downloadPath.setText(f"Pasta de Download: {self.config.path}")
            self.downloadPath.setToolTip(str(self.config.path))

        self.downloadPath.setGeometry(QRect(1, 205, 360, 10))
        self.downloadPath.adjustSize()
        self.downloadPath.setStyleSheet("font: 12px; padding-left: 2px; border: none; text-align: left;")
        self.downloadPath.clicked.connect(self.config.selectPath)
        self.config.pathChanged.connect(lambda path: self.downloadPath.setText(f'Pasta de Download: {path}'))

    @Slot()
    def updateQualityBox(self, formatType: str):
        formats = {
            ".mp4 (Vídeo)": self.mp4Types,
            ".mp3 (Áudio)": self.mp3Types
        }
        self.qualityBox.clear()
        self.qualityBox.addItems(formats[formatType])

    def downloadClicked(self):
        formatSelected, qualitySelected = self.fileFormatBox.currentText(), self.qualityBox.currentText()
        if self.config.path is None or not path.exists(self.config.path):
            QMessageBox.critical(self, "Pasta inválida", "<span style='font-size: 14px'><b>Selecione uma pasta de download válida antes de baixar.</b></span><br>"
                "<span style='font-size: 13px'>Clique no texto abaixo do botão \"Baixar\" para escolher a pasta de download.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return None

        if formatSelected == ".mp4 (Vídeo)":
            self.downloadThread = DownloadVideoThread(self.url, str(self.config.path), qualitySelected[:-1], 'mp4')
        else:
            self.downloadThread = DownloadVideoThread(self.url, str(self.config.path), qualitySelected[:-4], 'mp3', audioOnly=True)

        self.downloadButton.setDisabled(True)
        self.qualityBox.setDisabled(True)
        self.fileFormatBox.setDisabled(True)
        self.downloadPath.setDisabled(True)
        self.progress.setHidden(False)
        self.setFixedSize(360, 280)
        self.downloadPath.setGeometry(QRect(1, 255, 360, 10))
        self.downloadPath.adjustSize()

        self.downloadThread.finishedDownload.connect(lambda: QMessageBox.information(self, "Download concluído!", f"<span style='font-size: 16px'><b>Download concluído com sucesso!</b><br>Vídeo baixado: {self.title}</span>", QMessageBox.StandardButton.Ok))
        self.downloadThread.finishedDownload.connect(self.downloadThread.deleteLater)
        self.downloadThread.finishedDownload.connect(self.close)
        self.downloadThread.error.connect(lambda error: QMessageBox.critical(self, "Erro detectado!", f"Ocorreu um erro ao baixar o vídeo.\nErro: {error}", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok))
        self.downloadThread.progress.connect(lambda value: self.progress.setValue(value))
        self.downloadThread.start()

    def showConfigs(self):
        self.show()

class MainSettings(QWidget):
    themeChanged = Signal(str)
    pathChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.path = None
        self.settings = Settings()

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Configurações")
        self.setFixedSize(350, 220)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.themeLabel = QLabel('Tema:', self)
        self.themeLabel.setGeometry(QRect(3, 20, 70, 25))
        self.themeLabel.setStyleSheet("font: 19px")

        self.themeSelector = QComboBox(self)
        self.themeSelector.addItem("Claro")
        self.themeSelector.addItem("Escuro")
        self.themeSelector.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.themeSelector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.themeSelector.setCurrentText("Escuro" if self.settings.theme == 'dark' else "Claro")
        self.themeSelector.setGeometry(QRect(65, 18, 80, 20))
        self.themeSelector.setStyleSheet("font: 16px; border-radius: 6px")
        self.themeSelector.currentTextChanged.connect(self.themeChanged.emit)

        self.searchLimitLabel = QLabel("Limite de resultados:", self)
        self.searchLimitLabel.setGeometry(QRect(3, 70, 180, 25))
        self.searchLimitLabel.setStyleSheet("font: 19px;")

        self.searchLimit = QSpinBox(self)
        self.searchLimit.setGeometry(QRect(192, 70, 60, 25))
        self.searchLimit.setToolTip('Quanto maior a quantidade de resultados, mais lenta será a pesquisa.')
        self.searchLimit.setStyleSheet("font: 16px; border-radius: 6px;")
        self.searchLimit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.searchLimit.setMinimum(4)
        self.searchLimit.setMaximum(50)
        self.searchLimit.setValue(self.settings.searchlimit)

        self.downloadPathLabel = QLabel("Local de Download:", self)
        self.downloadPathLabel.setGeometry(QRect(3, 120, 170, 25))
        self.downloadPathLabel.setStyleSheet("font: 19px;")

        self.downloadPathButton = QPushButton("Clique aqui para definir", self)

        if self.settings.outputpath is not None:  # Caso já exista um caminho salvo nas configs, verifica se é válido e carrega
            try:
                self.path = Path(self.settings.outputpath)
            except Exception:
                pass
            else:
                if len(self.settings.outputpath) > 30:
                    self.downloadPathButton.setText('...' + self.settings.outputpath[-28:])
                    self.downloadPathButton.setStyleSheet('text-align: right;')
                else:
                    self.downloadPathButton.setText(self.settings.outputpath)
                    self.downloadPathButton.setStyleSheet('text-align: auto;')
                self.downloadPathButton.setToolTip(self.settings.outputpath)

        self.downloadPathButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.downloadPathButton.setGeometry(QRect(182, 120, 160, 30))
        self.downloadPathButton.clicked.connect(self.selectPath)

        self.saveButton = QPushButton("Salvar modificações", self)
        self.saveButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.saveButton.setGeometry(QRect(80, 165, 190, 35))
        self.saveButton.setStyleSheet("font: 19px bold \"Segoe UI\"; border-radius: 10px")
        self.saveButton.clicked.connect(self.saveConfigs)

    def showConfigs(self):
        self.show()

    def saveConfigs(self):
        self.settings.theme = self.themeSelector.currentText().lower()
        self.settings.searchlimit = self.searchLimit.value()
        self.settings.outputpath = str(self.path)

        self.close()

    def selectPath(self):
        fileDialog = QFileDialog.getExistingDirectory(self, "Selecione o diretório para download")

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
        self.pathChanged.emit(str(self.path))
        return fileDialog

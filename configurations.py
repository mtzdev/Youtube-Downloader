from PySide6.QtWidgets import QWidget, QFrame, QComboBox, QPushButton, QLabel, QFileDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QProgressBar, QSpinBox
from PySide6.QtCore import Qt, QRect, Signal, Slot
from pathlib import Path
from search import DownloadVideoThread
from os import path
from utils import Settings

class DownloadSettings(QWidget):
    def __init__(self, videoInfos: tuple, mainConfigs, i18n):
        super().__init__()
        self.title = videoInfos[0]
        self.channel = videoInfos[1]
        self.duration = videoInfos[2]
        self.url = videoInfos[4]
        self.config = mainConfigs
        self.i18n = i18n
        self.mp4Types = ["1080p", "720p", "480p", "360p", "240p"]
        self.mp3Types = ["320kbps", "256kbps", "192kbps", "128kbps", "96kbps"]

        self.setupUI()
        self.fileFormatBox.currentTextChanged.connect(lambda formatType: self.updateQualityBox(formatType))

    def setupUI(self):
        self.setWindowTitle(self.i18n.get("config_download"))
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

        infos = QLabel(f"{self.i18n.get('channel')}: {self.channel} • {self.i18n.get('duration')}: {durationtxt}")
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
        self.downloadButton.setText(self.i18n.get("download"))
        self.downloadButton.setGeometry(QRect(104, 145, 152, 41))
        self.downloadButton.setStyleSheet("font:24px bold \"Segoe UI\";")
        self.downloadButton.clicked.connect(self.downloadClicked)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(QRect(60, 210, 241, 25))
        self.progress.setValue(0)
        self.progress.setHidden(True)

        self.downloadPath = QPushButton(self.i18n.get("download_folder_not_defined"), self)
        if self.config.path is not None:
            self.downloadPath.setText(f"{self.i18n.get("download_folder")} {self.config.path}")
            self.downloadPath.setToolTip(str(self.config.path))

        self.downloadPath.setGeometry(QRect(1, 205, 360, 10))
        self.downloadPath.adjustSize()
        self.downloadPath.setStyleSheet("font: 12px; padding-left: 2px; border: none; text-align: left;")
        self.downloadPath.clicked.connect(self.config.selectPath)
        self.config.pathChanged.connect(lambda path: self.downloadPath.setText(f'{self.i18n.get("download_folder")} {path}'))

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
            QMessageBox.critical(self, self.i18n.get("invalid_folder"), self.i18n.get("invalid_folder_desc"), QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
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

        self.downloadThread.finishedDownload.connect(lambda: QMessageBox.information(self, self.i18n.get("download_finished"), f"{self.i18n.get("download_finished_desc")} {self.title}", QMessageBox.StandardButton.Ok))
        self.downloadThread.finishedDownload.connect(self.downloadThread.deleteLater)
        self.downloadThread.finishedDownload.connect(self.close)
        self.downloadThread.error.connect(lambda error: QMessageBox.critical(self, self.i18n.get("download_error"), f"{self.i18n.get("download_error_desc")} {error}", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok))
        self.downloadThread.progress.connect(lambda value: self.progress.setValue(value))
        self.downloadThread.start()

    def showConfigs(self):
        self.show()

class MainSettings(QWidget):
    themeChanged = Signal(str)
    pathChanged = Signal(str)

    def __init__(self, i18n):
        super().__init__()
        self.path = None
        self.settings = Settings()
        self.i18n = i18n
        self.restartPending = False

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle(self.i18n.get("configurations"))
        self.setFixedSize(380, 275)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.themeLabel = QLabel(self.i18n.get("theme"), self)
        self.themeLabel.move(10, 20)
        self.themeLabel.setMaximumWidth(90)
        self.themeLabel.setStyleSheet("font: 19px")

        self.themeSelector = QComboBox(self)
        self.themeSelector.addItem(self.i18n.get("light"), "light")
        self.themeSelector.addItem(self.i18n.get("dark"), "dark")
        self.themeSelector.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.themeSelector.setCursor(Qt.CursorShape.PointingHandCursor)
        if self.settings.theme == 'light':
            self.themeSelector.setCurrentText(self.i18n.get('light'))
        else:
            self.themeSelector.setCurrentText(self.i18n.get('dark'))

        offset = -16 if self.i18n.lang == 'pt_br' else -3
        self.themeSelector.move(self.themeLabel.width() + offset, 20)
        self.themeSelector.setFixedWidth(75)
        self.themeSelector.setStyleSheet("font: 16px; border-radius: 6px")
        self.themeSelector.currentTextChanged.connect(lambda: self.themeChanged.emit(self.themeSelector.currentData()))


        self.searchLimitLabel = QLabel(self.i18n.get("search_limit"), self)
        self.searchLimitLabel.move(10, 70)
        self.searchLimitLabel.setStyleSheet("font: 19px;")

        self.searchLimit = QSpinBox(self)
        offset = 102 if self.i18n.lang == 'pt_br' else 32
        self.searchLimit.move(self.searchLimitLabel.width() + offset, 70)
        self.searchLimit.setFixedWidth(60)
        self.searchLimit.setToolTip(self.i18n.get("search_limit_desc"))
        self.searchLimit.setStyleSheet("font: 16px; border-radius: 6px;")
        self.searchLimit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.searchLimit.setMinimum(4)
        self.searchLimit.setMaximum(50)
        self.searchLimit.setValue(self.settings.searchlimit)


        self.downloadPathLabel = QLabel(self.i18n.get("download_path"), self)
        self.downloadPathLabel.setStyleSheet("font: 19px;")
        self.downloadPathLabel.move(10, 120)

        self.downloadPathButton = QPushButton(self.i18n.get("click_to_define"), self)
        if self.settings.outputpath is not None:  # Caso já exista um caminho salvo nas configs, verifica se é válido e carrega
            try:
                self.path = Path(self.settings.outputpath)
            except Exception:
                pass
            else:
                max_len = 28 if self.i18n.lang == 'pt_br' else 33
                if len(self.settings.outputpath) > max_len:
                    self.downloadPathButton.setText('...' + self.settings.outputpath[-(max_len - 2):])
                    self.downloadPathButton.setStyleSheet('text-align: right;')
                else:
                    self.downloadPathButton.setText(self.settings.outputpath)
                    self.downloadPathButton.setStyleSheet('text-align: auto;')
                self.downloadPathButton.setToolTip(self.settings.outputpath)

        self.downloadPathButton.setCursor(Qt.CursorShape.PointingHandCursor)
        offset = 90 if self.i18n.lang == 'pt_br' else 58
        width = 180 if self.i18n.lang == 'pt_br' else 210
        self.downloadPathButton.move(self.downloadPathLabel.width() + offset, 120)
        self.downloadPathButton.setFixedSize(width, 30)
        self.downloadPathButton.clicked.connect(self.selectPath)


        self.languageLabel = QLabel(self.i18n.get("language"), self)
        self.languageLabel.setStyleSheet("font: 19px;")
        self.languageLabel.move(10, 170)

        self.languageSelector = QComboBox(self)
        self.languageSelector.addItem('Português')
        self.languageSelector.addItem('English')
        self.languageSelector.setStyleSheet("font: 16px; border-radius: 6px")
        offset = 24 if self.i18n.lang == 'pt_br' else 13
        self.languageSelector.move(self.languageLabel.width() + offset, 170)
        self.languageSelector.setFixedWidth(110)
        self.languageSelector.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.languageSelector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.languageSelector.setCurrentText('Português' if self.settings.language == 'pt_br' else 'English')
        self.languageSelector.currentTextChanged.connect(self.setLanguage)


        self.saveButton = QPushButton(self.i18n.get("save_modifications"), self)
        self.saveButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.saveButton.setGeometry(QRect(95, 225, 190, 35))
        self.saveButton.setStyleSheet("font: 19px bold \"Segoe UI\"; border-radius: 10px")
        self.saveButton.clicked.connect(self.saveConfigs)

    def showConfigs(self):
        self.show()

    def saveConfigs(self):
        self.settings.theme = self.themeSelector.currentText().lower()
        self.settings.searchlimit = self.searchLimit.value()
        if self.path:
            self.settings.outputpath = str(self.path)

        self.close()

    def selectPath(self):
        fileDialog = QFileDialog.getExistingDirectory(self, self.i18n.get("select_dir_to_download"))

        if fileDialog == "":
            return
        try:
            self.path = Path(fileDialog)
        except Exception:
            QMessageBox.critical(self, self.i18n.get("error"), self.i18n.get("download_dir_selection_error"), QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return

        max_len = 28 if self.i18n.lang == 'pt_br' else 33
        if len(str(self.path)) > max_len:
            self.downloadPathButton.setText('...' + str(self.path)[-(max_len - 2):])
            self.downloadPathButton.setStyleSheet('text-align: right;')
        else:
            self.downloadPathButton.setText(str(self.path))
            self.downloadPathButton.setStyleSheet('text-align: auto;')
        self.downloadPathButton.setToolTip(str(self.path))
        self.pathChanged.emit(str(self.path))
        return fileDialog

    def setLanguage(self, lang):
        langs = {
            'Português': 'pt_br',
            'English': 'en'
        }
        if lang in langs:
            self.settings.language = langs[lang]
            self.restartPending = True

    def closeEvent(self, event):
        if self.restartPending:
            QMessageBox.information(self, "Modificações pendentes | Pending Changes", "<span style='font-size: 14px;'><b>Reinicie o app</b> para aplicar as modificações.<br><b>Restart the app</b> to apply the changes.</span>", QMessageBox.StandardButton.Ok)

        event.accept()
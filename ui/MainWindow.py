# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowuYUjSQ.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(590, 521)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.searchBar = QLineEdit(self.centralwidget)
        self.searchBar.setObjectName(u"searchBar")
        self.searchBar.setGeometry(QRect(10, 10, 521, 41))
        self.searchBar.setFrame(True)
        self.configButton = QPushButton(self.centralwidget)
        self.configButton.setObjectName(u"configButton")
        self.configButton.setGeometry(QRect(538, 10, 42, 41))
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 60, 571, 435))
        self.listWidget.setStyleSheet(u"")
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.listWidget.setAutoScroll(False)
        self.listWidget.setTabKeyNavigation(True)
        self.loadingLabel = QLabel(self.centralwidget)
        self.loadingLabel.setObjectName(u"loadingLabel")
        self.loadingLabel.setEnabled(False)
        self.loadingLabel.setGeometry(QRect(235, 217, 120, 120))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.searchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Insira o link ou nome do v\u00eddeo para pesquisar.", None))
        self.configButton.setText("")
    # retranslateUi


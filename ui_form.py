# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 670)
        MainWindow.setStyleSheet(u"background-color:white;")
        self.actionLogin = QAction(MainWindow)
        self.actionLogin.setObjectName(u"actionLogin")
        self.actionLogout = QAction(MainWindow)
        self.actionLogout.setObjectName(u"actionLogout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 20, 1161, 141))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.logoGoRemote = QLabel(self.frame)
        self.logoGoRemote.setObjectName(u"logoGoRemote")
        self.logoGoRemote.setGeometry(QRect(350, 0, 521, 131))
        self.logoGoRemote.setPixmap(QPixmap(u"images/goremote.png"))
        self.logoGoRemote.setAlignment(Qt.AlignCenter)
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 170, 1161, 16))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 200, 291, 18))
        font = QFont()
        font.setFamilies([u"Ubuntu Sans"])
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color:black;\n"
"font-weight:bold;")
        self.inputBisnisSegmentasi = QLineEdit(self.centralwidget)
        self.inputBisnisSegmentasi.setObjectName(u"inputBisnisSegmentasi")
        self.inputBisnisSegmentasi.setGeometry(QRect(320, 190, 291, 31))
        self.inputBisnisSegmentasi.setStyleSheet(u"color:black;")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 240, 261, 18))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color:black;\n"
"font-weight:bold;")
        self.inputLimit = QLineEdit(self.centralwidget)
        self.inputLimit.setObjectName(u"inputLimit")
        self.inputLimit.setGeometry(QRect(840, 190, 291, 31))
        self.inputLimit.setStyleSheet(u"color:black;")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(700, 200, 131, 18))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"color:black;\n"
"font-weight:bold;")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(700, 240, 121, 18))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"color:black;\n"
"font-weight:bold;")
        self.inputGeolokasi = QLineEdit(self.centralwidget)
        self.inputGeolokasi.setObjectName(u"inputGeolokasi")
        self.inputGeolokasi.setGeometry(QRect(320, 240, 291, 31))
        self.inputGeolokasi.setStyleSheet(u"color:black;")
        self.inputDelay = QLineEdit(self.centralwidget)
        self.inputDelay.setObjectName(u"inputDelay")
        self.inputDelay.setGeometry(QRect(840, 240, 291, 31))
        self.inputDelay.setStyleSheet(u"color:black;")
        self.btnSearch = QPushButton(self.centralwidget)
        self.btnSearch.setObjectName(u"btnSearch")
        self.btnSearch.setGeometry(QRect(20, 290, 88, 26))
        self.btnSearch.setStyleSheet(u"color:black;\n"
"color: rgb(14, 1, 1);\n"
"font-weight:bold;")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(130, 290, 88, 26))
        self.pushButton_2.setStyleSheet(u"color:black;\n"
"color: rgb(14, 1, 1);\n"
"font-weight:bold;")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(240, 290, 88, 26))
        self.pushButton_3.setStyleSheet(u"color:black;\n"
"color: rgb(14, 1, 1);\n"
"font-weight:bold;")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 330, 1161, 271))
        self.tabWidget.setStyleSheet(u"font-weight:bold;\n"
"color:white;\n"
"border-color: rgb(255, 255, 255);\n"
"background-color: rgb(40, 32, 32)")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tableWidget = QTableWidget(self.tab)
        if (self.tableWidget.columnCount() < 11):
            self.tableWidget.setColumnCount(11)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        if (self.tableWidget.rowCount() < 2):
            self.tableWidget.setRowCount(2)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setItem(0, 4, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setItem(0, 5, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setItem(0, 6, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setItem(0, 7, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setItem(0, 8, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setItem(0, 9, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setItem(0, 10, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem22)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 10, 1131, 211))
        self.tableWidget.setStyleSheet(u"border: solid 1px rgb(255, 255, 255);\n"
"")
        self.tableWidget.setFrameShape(QFrame.Panel)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 23))
        self.menubar.setStyleSheet(u"color:white;\n"
"font-weight:bold;\n"
"background-color: rgb(6, 37, 210);")
        self.menuAccount = QMenu(self.menubar)
        self.menuAccount.setObjectName(u"menuAccount")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAccount.menuAction())
        self.menuAccount.addAction(self.actionLogin)
        self.menuAccount.addAction(self.actionLogout)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLogin.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.actionLogout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.logoGoRemote.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Bisnis Segmentasi (Hotel/Restaurant):", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Geolokasi (Jagakarsa/Depok/dll):", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Limit Pencarian:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Delay (detik):", None))
        self.btnSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nama", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Rate", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"No.Telepon", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Email", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Alamat", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Instagram", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Facebook", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"TikTok", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Youtube", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Linkedin", None));
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Linkedin", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem11 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Hotel Indonesia", None));
        ___qtablewidgetitem12 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem13 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem14 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem15 = self.tableWidget.item(0, 4)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem16 = self.tableWidget.item(0, 5)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem17 = self.tableWidget.item(0, 7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem18 = self.tableWidget.item(0, 8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem19 = self.tableWidget.item(0, 9)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem20 = self.tableWidget.item(0, 10)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"1", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Hasil Terkini", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Riwayat Pencarian", None))
        self.menuAccount.setTitle(QCoreApplication.translate("MainWindow", u"Account", None))
    # retranslateUi


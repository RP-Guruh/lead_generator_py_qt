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
    QProgressBar, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 695)
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
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.logoGoRemote = QLabel(self.frame)
        self.logoGoRemote.setObjectName(u"logoGoRemote")
        self.logoGoRemote.setGeometry(QRect(350, 0, 521, 131))
        self.logoGoRemote.setPixmap(QPixmap(u"images/goremote.png"))
        self.logoGoRemote.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 170, 1161, 16))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 200, 271, 18))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color:black;\n"
"font-weight:bold;")
        self.inputBisnisSegmentasi = QLineEdit(self.centralwidget)
        self.inputBisnisSegmentasi.setObjectName(u"inputBisnisSegmentasi")
        self.inputBisnisSegmentasi.setGeometry(QRect(320, 200, 291, 21))
        self.inputBisnisSegmentasi.setStyleSheet(u"color:black;")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 240, 261, 18))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color:black;\n"
"font-weight:bold;")
        self.inputLimit = QLineEdit(self.centralwidget)
        self.inputLimit.setObjectName(u"inputLimit")
        self.inputLimit.setGeometry(QRect(840, 200, 291, 20))
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
        self.inputGeolokasi.setGeometry(QRect(320, 240, 291, 21))
        self.inputGeolokasi.setStyleSheet(u"color:black;")
        self.inputDelay = QLineEdit(self.centralwidget)
        self.inputDelay.setObjectName(u"inputDelay")
        self.inputDelay.setGeometry(QRect(840, 230, 291, 21))
        self.inputDelay.setStyleSheet(u"color:black;")
        self.btnSearch = QPushButton(self.centralwidget)
        self.btnSearch.setObjectName(u"btnSearch")
        self.btnSearch.setGeometry(QRect(20, 280, 88, 31))
        self.btnSearch.setStyleSheet(u"color:black;\n"
"color: rgb(14, 1, 1);\n"
"font-weight:bold;")
        self.btnCancel = QPushButton(self.centralwidget)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.setGeometry(QRect(130, 280, 88, 31))
        self.btnCancel.setStyleSheet(u"color:black;\n"
"color: rgb(14, 1, 1);\n"
"font-weight:bold;")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 330, 1161, 271))
        self.tabWidget.setStyleSheet(u"font-weight:bold;\n"
"color:white;\n"
"border-color: rgb(255, 255, 255);\n"
"background-color: rgb(54, 54, 54)")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tableTerkini = QTableWidget(self.tab)
        if (self.tableTerkini.columnCount() < 12):
            self.tableTerkini.setColumnCount(12)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableTerkini.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        if (self.tableTerkini.rowCount() < 2):
            self.tableTerkini.setRowCount(2)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableTerkini.setItem(0, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableTerkini.setItem(0, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableTerkini.setItem(1, 0, __qtablewidgetitem14)
        self.tableTerkini.setObjectName(u"tableTerkini")
        self.tableTerkini.setGeometry(QRect(10, 10, 1131, 211))
        self.tableTerkini.setStyleSheet(u"border: solid 1px rgb(255, 255, 255);\n"
"")
        self.tableTerkini.setFrameShape(QFrame.Shape.Panel)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tableRiwayatPencarian = QTableWidget(self.tab_2)
        if (self.tableRiwayatPencarian.columnCount() < 7):
            self.tableRiwayatPencarian.setColumnCount(7)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableRiwayatPencarian.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableRiwayatPencarian.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableRiwayatPencarian.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableRiwayatPencarian.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableRiwayatPencarian.setHorizontalHeaderItem(4, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableRiwayatPencarian.setHorizontalHeaderItem(5, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableRiwayatPencarian.setHorizontalHeaderItem(6, __qtablewidgetitem21)
        if (self.tableRiwayatPencarian.rowCount() < 2):
            self.tableRiwayatPencarian.setRowCount(2)
        self.tableRiwayatPencarian.setObjectName(u"tableRiwayatPencarian")
        self.tableRiwayatPencarian.setGeometry(QRect(10, 10, 1131, 211))
        self.tableRiwayatPencarian.setStyleSheet(u"border: solid 1px rgb(255, 255, 255);\n"
"")
        self.tableRiwayatPencarian.setFrameShape(QFrame.Shape.Panel)
        self.tabWidget.addTab(self.tab_2, "")
        self.btnDownload = QPushButton(self.centralwidget)
        self.btnDownload.setObjectName(u"btnDownload")
        self.btnDownload.setGeometry(QRect(240, 280, 101, 31))
        self.btnDownload.setStyleSheet(u"color:black;\n"
"color: rgb(14, 1, 1);\n"
"font-weight:bold;")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(20, 610, 1161, 21))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"   border: 2px solid #5e5e5e;\n"
"   border-radius: 5px; \n"
"   background-color: rgb(56, 56, 56);\n"
"   text-align: center;\n"
"   color: white;\n"
"   font-weight: bold;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"	background-color: rgb(0, 99, 204);\n"
"}\n"
"")
        self.progressBar.setValue(24)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        self.menubar.setStyleSheet(u"color:white;\n"
"font-weight:bold;\n"
"background-color: rgb(0, 99, 204);")
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

        self.tabWidget.setCurrentIndex(1)


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
        self.btnCancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        ___qtablewidgetitem = self.tableTerkini.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nama", None));
        ___qtablewidgetitem1 = self.tableTerkini.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Rate", None));
        ___qtablewidgetitem2 = self.tableTerkini.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Jumlah Ulasan", None));
        ___qtablewidgetitem3 = self.tableTerkini.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"No.Telepon", None));
        ___qtablewidgetitem4 = self.tableTerkini.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Email", None));
        ___qtablewidgetitem5 = self.tableTerkini.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Website", None));
        ___qtablewidgetitem6 = self.tableTerkini.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Alamat", None));
        ___qtablewidgetitem7 = self.tableTerkini.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Instagram", None));
        ___qtablewidgetitem8 = self.tableTerkini.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Facebook", None));
        ___qtablewidgetitem9 = self.tableTerkini.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Tiktok", None));
        ___qtablewidgetitem10 = self.tableTerkini.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Linkedln", None));
        ___qtablewidgetitem11 = self.tableTerkini.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Youtube", None));

        __sortingEnabled = self.tableTerkini.isSortingEnabled()
        self.tableTerkini.setSortingEnabled(False)
        self.tableTerkini.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Hasil Terkini", None))
        ___qtablewidgetitem12 = self.tableRiwayatPencarian.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem13 = self.tableRiwayatPencarian.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Bisnis Segmentasi", None));
        ___qtablewidgetitem14 = self.tableRiwayatPencarian.horizontalHeaderItem(2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Geolokasi", None));
        ___qtablewidgetitem15 = self.tableRiwayatPencarian.horizontalHeaderItem(3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Limit Pencarian", None));
        ___qtablewidgetitem16 = self.tableRiwayatPencarian.horizontalHeaderItem(4)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Jumlah didapat", None));
        ___qtablewidgetitem17 = self.tableRiwayatPencarian.horizontalHeaderItem(5)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Delay (detik)", None));
        ___qtablewidgetitem18 = self.tableRiwayatPencarian.horizontalHeaderItem(6)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Tanggal Pencarian", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Riwayat Pencarian", None))
        self.btnDownload.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.menuAccount.setTitle(QCoreApplication.translate("MainWindow", u"Account", None))
    # retranslateUi


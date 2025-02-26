# This Python file uses the following encoding: utf-8
import sys
import pandas as pd
import os
import webbrowser
from datetime import datetime
from databasesqlite import databasesqlite
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QLabel, QFrame, QLineEdit
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Slot, Qt
from ui_form import Ui_MainWindow
from validateform import validateform
from tablehelper import TableHelper
from api import API
from checkuuidos import checkuuidos
from log import Logger

class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # inisialisasi log
        self.logging = Logger()
        self.logging.write_logging("Started application")


        # Title Aplikasi
        self.setWindowTitle("Lead Generator by GoRemote")

        # disabled tombol cancel
        self.ui.btnCancel.setEnabled(False)

        # API INSTANCE
        self.api_instance = API(self.ui)
        self.uuidos = checkuuidos()

        # Simpan koneksi database
        # Buat objek databasesqlite dengan QObject
        self.db = databasesqlite()
        self.load_results()
        self.is_login = self.db.get_session()

        if self.is_login == None:
            self.ui.lblStatusLogin.setText("Not logged in")
        else:
            token_login = self.is_login[0]
            sisa = self.api_instance.sisa_quota(token_login)
            self.ui.lblStatusLogin.setText("Logged in")
            self.ui.lblTitleSisaQuota.setText("Sisa Kuota : ")
            self.ui.lblSisaKuota.setText(str(sisa))



        # Atur ukuran default
        width = 1200
        height = 680
        self.setFixedSize(width, height)

        # Atur gambar logo lead generator
        self.ui.logoGoRemote.setScaledContents(True)

        self.ui.btnSearch.clicked.connect(self.on_btn_search_clicked)
        self.ui.btnDownload.clicked.connect(self.download_current_result)
        self.ui.btnCancel.clicked.connect(self.cancel_scrapping)
        self.ui.tableRiwayatPencarian.cellDoubleClicked.connect(self.on_table_double_click)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.actionLogin.triggered.connect(self.login)
        self.ui.actionLogout.triggered.connect(self.logout)

    def on_btn_search_clicked(self):
        #Tangkap input dari form
        bisnis_segmentasi = self.ui.inputBisnisSegmentasi.text()
        geolokasi = self.ui.inputGeolokasi.text()
        limit_pencarian = self.ui.inputLimit.text()
        delay_pencarian = self.ui.inputDelay.text()
        #kirim ke validasi untuk dicek
        is_valid, message = validateform.validate_form(bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian)

        # Menampilkan pesan hasil validasi
        if not is_valid:
            self.show_error(message)
        else:
            uuid = self.uuidos.get_uuid()
            self.api_instance.check_limit(uuid, bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian)

    def login(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Sign In")
        dlg.setFixedSize(300, 250)

        layout = QVBoxLayout()

        # Logo
        logo = QLabel()
        pixmap = QPixmap("./images/goremote.png")  # Pastikan path gambar benar
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)  # Opsional: agar gambar menyesuaikan ukuran label
        logo.setFixedSize(210, 70)
        logo.setAlignment(Qt.AlignCenter)  # Memastikan logo sejajar horizontal di tengah
        layout.addWidget(logo, alignment=Qt.AlignHCenter)  # Tambahkan logo di atas

        # separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)  # Garis horizontal
        separator.setFrameShadow(QFrame.Sunken)  # Efek 3D
        separator.setFixedHeight(2)  # Ketebalan garis
        layout.addWidget(separator)

        # Input Email
        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_input.setStyleSheet("color:black;")
        email_input.setFixedHeight(35)
        layout.addWidget(email_input)

        # Input Password
        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setEchoMode(QLineEdit.Password)  # Menyembunyikan password
        password_input.setStyleSheet("color:black;")
        password_input.setFixedHeight(35)
        layout.addWidget(password_input)

        # Tombol Login
        login_button = QPushButton("Login")
        login_button.setFixedHeight(35)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 99, 204);
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(0, 130, 255); /* Lebih terang saat hover */
            }
            QPushButton:pressed {
                background-color: rgb(0, 80, 180); /* Lebih gelap saat ditekan */
            }
        """)
        layout.addWidget(login_button)
        #login_button.clicked.connect(lambda: self.login_process(email_input, password_input))
        login_button.clicked.connect(dlg.accept)

        # Link "Belum mendaftar?"
        register_label = QLabel('<a style="color:rgb(0, 99, 204);" href="https://goremote.id/leads-generator/">Belum mendaftar?</a>')
        register_label.setTextFormat(Qt.RichText)  # Aktifkan HTML
        register_label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # Bisa diklik
        register_label.setOpenExternalLinks(True)  # Tangani klik sendiri
        register_label.setAlignment(Qt.AlignCenter)
        # Menangani klik pada link
        register_label.linkActivated.connect(self.open_register_page)
        layout.addWidget(register_label)

        layout.addStretch()  # Tambahkan stretch di atas agar logo terdorong ke atas
        dlg.setLayout(layout)
        # Tampilkan dialog dan cek hasilnya
        if dlg.exec() == QDialog.Accepted:
            self.login_process(email_input, password_input)

    def logout(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Sign Out")
        dlg.setFixedSize(300, 100)

        # Layout utama
        layout = QVBoxLayout()

        # Pesan konfirmasi
        message = QLabel("Anda yakin ingin logout?")
        message.setStyleSheet("color:black;")
        layout.addWidget(message)

        # Layout untuk tombol
        button_layout = QHBoxLayout()

        # Tombol "Ya"
        yes_button = QPushButton("Ya")
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 99, 204);
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(0, 130, 255);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgb(0, 80, 180); /* Lebih gelap saat ditekan */
            }
        """)

        yes_button.clicked.connect(dlg.accept)  # Menutup dialog dengan status 'Accepted'

        # Tombol "Cancel"
        cancel_button = QPushButton("Cancel")

        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(150, 150, 150);
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(170, 170, 170); /* Sedikit lebih terang saat hover */
            }
            QPushButton:pressed {
                background-color: rgb(120, 120, 120); /* Lebih gelap saat ditekan */
            }
        """)

        cancel_button.clicked.connect(dlg.reject)  # Menutup dialog dengan status 'Rejected'

        # Tambahkan tombol ke layout horizontal
        button_layout.addWidget(yes_button)
        button_layout.addWidget(cancel_button)

        # Tambahkan semua layout ke dalam dialog
        layout.addLayout(button_layout)
        dlg.setLayout(layout)

        # Tampilkan dialog dan cek hasilnya
        if dlg.exec() == QDialog.Accepted:
            self.logout_process()

    def login_process(self, email, password):
        email = email.text()
        password = password.text()

        is_valid, message = validateform.validate_login_form(email, password)

        # Menampilkan pesan hasil validasi
        if not is_valid:
            self.show_error(message)
        else:
            self.api_instance.login_api(email, password)

    def logout_process(self):
        self.api_instance.logout_api()

    def cancel_scrapping(self):
        self.api_instance.cancel_process()

    def open_register_page(self, link):
        webbrowser.open(link)

    def on_table_double_click(self, row, column):
        if column == 0:
            item = self.ui.tableRiwayatPencarian.item(row, column)
            id = item.text()
            results = self.db.get_data_byid(id)

            # Buat dialog
            dlg = QDialog(self)
            dlg.setWindowTitle("Detail Riwayat Pencarian")
            dlg.setFixedSize(1000, 500)

            # Header tabel
            headers = [
                "Nama Lokasi", "Rate", "Jumlah Ulasan", "No.Telepon", "Email", "Website", "Alamat",
                "Instagram", "Facebook", "Twitter", "Linkdln", "YouTube", "Tiktok", "Link Gmaps"
            ]

            # Buat tabel
            table = QTableWidget()
            table.setStyleSheet("color:black; border: solid 1px rgb(255, 255, 255);")
            table.setColumnCount(len(headers))
            table.setRowCount(1)  # Hanya 1 baris dari data yang dipilih
            table.setHorizontalHeaderLabels(headers)

            # Isi data ke dalam tabel
            TableHelper.populate_table(table, results)

            # Tombol Download (tanpa fungsi)
            style_button = """
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: bold;
                border: 2px solid #005A9E;
            }
            QPushButton:hover {
                background-color: #005A9E;
                border: 2px solid #003F73;
            }
            QPushButton:pressed {
                background-color: #004A8F;
                border: 2px solid #002F5E;
            }
            """
            btn_download = QPushButton("Download")
            btn_download.setStyleSheet(style_button)
            btn_download.clicked.connect(lambda: self.download_by_id(id))


            # Layout tombol di atas tabel
            layout = QVBoxLayout()
            btn_layout = QHBoxLayout()
            btn_layout.addWidget(btn_download)

            # Tambahkan ke layout utama
            layout.addLayout(btn_layout)
            layout.addWidget(table)
            dlg.setLayout(layout)

            dlg.exec()

    def download_current_result(self):
        search_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_current = self.db.get_current_result()
        # Tentukan folder Downloads berdasarkan sistem operasi
        if sys.platform.startswith("win"):  # Windows
            downloads_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
        elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):  # Linux & macOS
            downloads_folder = os.path.join(os.environ["HOME"], "Downloads")
        else:
            downloads_folder = os.getcwd()  # Jika tidak dikenali, simpan di folder saat ini
        # Path lengkap untuk file Excel
        file_path = os.path.join(downloads_folder, f"searching_current_data_{search_date}.xlsx")

        df = pd.DataFrame(results_current, columns=[
            "nama_lokasi", "rate", "jumlah_ulasan", "no_telepon", "email", "website", "alamat", "instagram", "facebook", "twitter", "linkedln", "youtube", "tiktok", "link"
        ])
        # Simpan ke Excel
        df.to_excel(file_path, index=False)
        message = f"File berhasil disimpan di: {file_path}"
        self.success_download(message)

    def download_by_id(self,id):
        search_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_current = self.db.get_data_byid(id)
        # Tentukan folder Downloads berdasarkan sistem operasi
        if sys.platform.startswith("win"):  # Windows
            downloads_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
        elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):  # Linux & macOS
            downloads_folder = os.path.join(os.environ["HOME"], "Downloads")
        else:
            downloads_folder = os.getcwd()  # Jika tidak dikenali, simpan di folder saat ini
        # Path lengkap untuk file Excel
        file_path = os.path.join(downloads_folder, f"data_{id}_{search_date}.xlsx")

        df = pd.DataFrame(results_current, columns=[
            "nama_lokasi", "rate", "jumlah_ulasan", "no_telepon", "email", "website", "alamat", "instagram", "facebook", "twitter", "linkedln", "youtube", "tiktok", "link"
        ])
        # Simpan ke Excel
        df.to_excel(file_path, index=False)
        message = f"File berhasil disimpan di: {file_path}"
        self.success_download(message)

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setStyleSheet("QLabel { color : black; } QPushButton { color : black; }")
        msg.exec()

    def success_download(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Download successfull")
        msg.setText(message)
        msg.setStyleSheet("QLabel { color : black; } QPushButton { color : black; }")
        msg.exec()

    @Slot()
    def load_results(self):
        results_current = self.db.get_current_result()
        results_history = self.db.get_search_history()
        TableHelper.populate_table(self.ui.tableTerkini, results_current)
        TableHelper.populate_table(self.ui.tableRiwayatPencarian, results_history)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

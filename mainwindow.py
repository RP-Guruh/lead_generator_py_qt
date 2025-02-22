# This Python file uses the following encoding: utf-8
import sys
import pandas as pd
import os
import subprocess
from datetime import datetime
from databasesqlite import databasesqlite
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton
from PySide6.QtCore import Slot
from ui_form import Ui_MainWindow
from validateform import validateform
from scrapping import scrapping
from tablehelper import TableHelper

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # disabled tombol cancel
        self.ui.btnCancel.setEnabled(False)

        # Hubungkan signal `dataInserted` dengan method `load_results`
        self.db = databasesqlite()

        # Panggil untuk menampilkan data awal
        self.load_results()

        # Title Aplikasi
        self.setWindowTitle("Lead Generator by GoRemote")

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
            scraper = scrapping(self.ui)
            scraper.run_scrapping(bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian)


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
            btn_download = QPushButton("Download")
            btn_download.setStyleSheet("color:white; font-weight:bold; background-color: blue;")
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
        search_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        search_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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

    def cancel_scrapping(self):
        print("cancel diklik")

    def show_error(self, message):
        # Menampilkan pesan kesalahan menggunakan QMessageBox
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

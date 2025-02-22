# This Python file uses the following encoding: utf-8
import sys
import pandas as pd
import os
import subprocess
from databasesqlite import databasesqlite
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
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

        # Hubungkan signal `dataInserted` dengan method `load_results`
        self.db = databasesqlite()

        # Panggil untuk menampilkan data awal
        self.load_results()

        # Title Aplikasi
        self.setWindowTitle("Lead Generator by GoRemote")

        # Atur ukuran default
        width = 1200
        height = 670
        self.setFixedSize(width, height)

        # Atur gambar logo lead generator
        self.ui.logoGoRemote.setScaledContents(True)

        self.ui.btnSearch.clicked.connect(self.on_btn_search_clicked)
        self.ui.btnDownload.clicked.connect(self.download_current_result)


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
            print("Form valid!")

    def download_current_result(self):

        results_current = self.db.get_current_result()
        print(f"Jumlah kolom dalam data: {len(results_current[0])}")

        # Tentukan folder Downloads berdasarkan sistem operasi
        if sys.platform.startswith("win"):  # Windows
            downloads_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
        elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):  # Linux & macOS
            downloads_folder = os.path.join(os.environ["HOME"], "Downloads")
        else:
            downloads_folder = os.getcwd()  # Jika tidak dikenali, simpan di folder saat ini
        # Path lengkap untuk file Excel
        file_path = os.path.join(downloads_folder, "searching_current_data.xlsx")

        df = pd.DataFrame(results_current, columns=[
            "nama_lokasi", "rate", "jumlah_ulasan", "no_telepon", "email", "website", "alamat", "instagram", "facebook", "twitter", "linkedln", "youtube", "tiktok"
        ])
        # Simpan ke Excel
        df.to_excel(file_path, index=False)
        message = f"File berhasil disimpan di: {file_path}"
        self.success_download(message)


    def cancel_scrapping(self):
        scraper = scrapping(self.ui)
        scraper.cancel_scrapping()

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

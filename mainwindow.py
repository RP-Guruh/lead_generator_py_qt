# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from validateform import validateform  # Mengimpor kelas validateform
from scrapping import scrapping

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Title Aplikasi
        self.setWindowTitle("Lead Generator by GoRemote")

        # Atur ukuran default
        width = 1200
        height = 670
        self.setFixedSize(width, height)

        # Atur gambar logo lead generator
        self.ui.logoGoRemote.setScaledContents(True)

        self.ui.btnSearch.clicked.connect(self.on_btn_search_clicked)

        #modifikasi button
        style_button = """
        QPushButton {
            background-color: #0078D7;
            color: white;
            border-radius: 8px;
            padding: 8px 18px;
            font-size: 13px;
            font-weight: bold;
            border: 2px solid #005A9E;
            box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
        }
        QPushButton:hover {
            background-color: #005A9E;
            border: 2px solid #003F73;
        }
        QPushButton:pressed {
            background-color: #004A8F;
            border: 2px solid #002F5E;
            box-shadow: none;
        }
        """
        self.ui.btnDownload.setStyleSheet(style_button)
        self.ui.btnSearch.setStyleSheet(style_button)
        self.ui.btnCancel.setStyleSheet(style_button)



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
            scrapping.run_scrapping(bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian)
            print("Form valid!")

    def show_error(self, message):
        # Menampilkan pesan kesalahan menggunakan QMessageBox
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setStyleSheet("QLabel { color : black; } QPushButton { color : black; }")
        msg.exec()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

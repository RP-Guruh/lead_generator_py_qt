import requests
import json
from databasesqlite import databasesqlite
from PySide6.QtWidgets import QMessageBox

class API:
    URLAPI = "https://lead-generator.goremote.id/api"

    def __init__(self):
        self.database = databasesqlite()  # Inisialisasi database
        self.logger = self.get_logger()  # Inisialisasi logger

    def get_logger(self):
        """Fungsi dummy logger untuk menghindari error jika logger belum tersedia"""
        class Logger:
            def log_info(self, message):
                print("[INFO]", message)
            def log_error(self, message):
                print("[ERROR]", message)
        return Logger()

    def show_message(self, title, message, icon=QMessageBox.Information):
        """Menampilkan QMessageBox dengan pesan tertentu"""
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def login_api(self, email, password):
        url = f"{self.URLAPI}/login"
        payload = {
            "email": email,
            "password": password
        }

        try:
            # Mengirim request POST ke API dengan timeout 10 detik
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)

            # Cek apakah login berhasil
            if response.status_code == 200:
                data = response.json()
                is_login = "Y"

                # Simpan sesi pengguna ke database
                self.database.save_session_login(
                    data["user"]["id"],
                    data["token"],
                    data["user"]["name"],
                    data["user"]["email"],
                    is_login
                )

                self.logger.log_info("Login berhasil")
                self.show_message("Login Berhasil", f"Selamat datang, {data['user']['name']}!", QMessageBox.Information)

            elif response.status_code == 401:
                # Login gagal (email/password salah)
                error_message = "Login gagal, pastikan email/password benar dan terdaftar"
                self.logger.log_error(error_message)
                self.show_message("Login Gagal", error_message, QMessageBox.Warning)

            else:
                # Kesalahan lain dari API
                error_message = f"API Error - Status: {response.status_code}, Body: {response.text}"
                self.logger.log_error(error_message)
                self.show_message("Kesalahan API", error_message, QMessageBox.Critical)

        except requests.Timeout:
            # Menangani timeout error
            error_message = "Timeout error occurred during login"
            self.logger.log_error(error_message)
            self.show_message("Timeout", error_message, QMessageBox.Warning)

        except requests.ConnectionError:
            # Menangani error kegagalan koneksi
            error_message = "Connection failed during login"
            self.logger.log_error(error_message)
            self.show_message("Koneksi Gagal", error_message, QMessageBox.Critical)

        except Exception as e:
            # Menangani error lainnya
            error_message = f"An unexpected error occurred during login: {str(e)}"
            self.logger.log_error(error_message)
            self.show_message("Error", error_message, QMessageBox.Critical)

    def logout_api(self):
        url = f"{self.URLAPI}/logout"

        # Ambil token dari sesi database jika ada
        session = self.database.get_session()
        token = session[0] if session else None
        # Cek apakah token tersedia sebelum logout
        if not token:
            self.show_message("Logout Gagal", "Tidak ada sesi login yang ditemukan.", QMessageBox.Warning)
            return

        try:
            # Mengirim request DELETE ke API dengan token autentikasi
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            response = requests.delete(url, headers=headers, timeout=10)

            # Cek apakah logout berhasil
            if response.status_code == 200:
                # Hapus sesi pengguna dari database
                self.database.delete_session()

                self.logger.log_info("Logout berhasil")
                self.show_message("Logout Berhasil", "Anda telah logout.", QMessageBox.Information)

            elif response.status_code == 401:
                error_message = "Logout gagal, harap ulangi kembali"
                self.logger.log_error(error_message)
                self.show_message("Logout Gagal", error_message, QMessageBox.Warning)

            else:
                # Kesalahan lain dari API
                error_message = f"API Error - Status: {response.status_code}, Body: {response.text}"
                self.logger.log_error(error_message)
                self.show_message("Kesalahan API", error_message, QMessageBox.Critical)

        except requests.Timeout:
            # Menangani timeout error
            error_message = "Timeout error occurred during logout"
            self.logger.log_error(error_message)
            self.show_message("Timeout", error_message, QMessageBox.Warning)

        except requests.ConnectionError:
            # Menangani error kegagalan koneksi
            error_message = "Connection failed during logout"
            self.logger.log_error(error_message)
            self.show_message("Koneksi Gagal", error_message, QMessageBox.Critical)

        except Exception as e:
            # Menangani error lainnya
            error_message = f"An unexpected error occurred during logout: {str(e)}"
            self.logger.log_error(error_message)
            self.show_message("Error", error_message, QMessageBox.Critical)



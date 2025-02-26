from databasesqlite import databasesqlite
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject
from scrapping import scrapping
from checkuuidos import checkuuidos
import webbrowser
import requests
import json

class API(QObject):
    URLAPI = "https://lead-generator.goremote.id/api"

    def __init__(self, ui):
        super().__init__()
        self.database = databasesqlite()
        self.logger = self.get_logger()
        self.ui = ui
        self.id_simpan_request = None
        self.uuidos = checkuuidos()

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
                self.ui.lblStatusLogin.setText("You logged in")

                self.is_login = self.database.get_session()
                token_login = self.is_login[0]
                sisa = self.sisa_quota(token_login)
                self.ui.lblTitleSisaQuota.setText("Sisa Kuota : ")
                self.ui.lblSisaKuota.setText(str(sisa))

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
                self.ui.lblStatusLogin.setText("Logged out")
                self.ui.lblTitleSisaQuota.setText("")
                self.ui.lblSisaKuota.setText("")

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

    def check_limit(self, uuid, bisnis_segmentasi, geolokasi, request_quota, delay_pencarian):

        # kita cek dulu dia sudah login atau belum
        session = self.database.get_session()
        token = session[0] if session else None
        # kalau sudah login artinya dia sudah punya akun dan mendaftar jadinya ngecek pakai limit berlangganan bukan dari uuid
        if token:
            url = f"{self.URLAPI}/search/request"
            payload = {
                "query": bisnis_segmentasi,
                "place": geolokasi,
                "request_quota": request_quota
            }
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                data = response.json()
                # Cek apakah limit masih cukup

                # limit gak cukup alias udah abis
                if response.status_code == 402:
                    if data['data']['sisa_quota'] < 0:
                        title = "Paket Anda Telah Berakhir"
                        pesan = "Masa aktif paket Anda telah habis. Silakan perpanjang langganan untuk terus menggunakan layanan."
                    else:
                        title = 'Kuota Hampir Habis!'
                        pesan = (f"Kuota Anda tersisa {data['data']['sisa_quota']} data. "
                                 "Tambahkan kuota untuk dapat mengakses lebih banyak data.")
                    self.show_message(title, pesan, QMessageBox.Critical)
                    webbrowser.open("https://goremote.id/leads-generator/")

                if response.status_code == 200:
                    self.id_simpan_request = data["data"]["id"]
                    #jalanin scrapping disini
                    scraper = scrapping(self.ui)
                    scraper.run_scrapping(bisnis_segmentasi, geolokasi, request_quota, delay_pencarian, self.id_simpan_request)

            except Exception as e:
                print(e)
        else:
            #belum login berarti check dari uuid
            os = self.uuidos.get_os_name()
            arsitektur = self.uuidos.get_architecture()
            uuid = self.uuidos.get_uuid()
            self.guest_request(os, arsitektur, uuid, bisnis_segmentasi, geolokasi, request_quota, delay_pencarian)

    def simpan_riwayat_pencarian(self, hasil_didapat, id_simpan_riwayat):
        print("masuk ke sini untuk update")
        session = self.database.get_session()
        token = session[0] if session else None

        if not token:
            print("Token tidak ditemukan, pastikan user sudah login.")
            return

        url = f"{self.URLAPI}/search/response"
        payload = {
          "id": id_simpan_riwayat,
          "response_quota": hasil_didapat
        }

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            response = requests.post(url, json=payload, headers=headers, timeout=10)

            response.raise_for_status()  # Akan error jika status bukan 2xx

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Unexpected Error: {err}")

    def guest_request(self, os, arsitektur, uuid, bisnis_segmentasi, geolokasi, request_quota, delay_pencarian):
        # cek dulu uuid nya udah kedatar belum
        """ Cek apakah UUID sudah terdaftar dan handle batasan limit """
        url = f"{self.URLAPI}/guest-request?uuid_os={uuid}"
        try:
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Error: Server mengembalikan status {response.status_code}")
                return

            data = response.json()  # Pastikan response.json() dipanggil
            user_data = data.get("data", {})

            if not user_data:  # Jika 'data' kosong
                url = f"{self.URLAPI}/guest-request"
                payload = {
                    "uuid_os": uuid,
                    "os_name": os,
                    "arch_os": arsitektur,
                    "used_limit": request_quota
                }
                headers = {
                    "Content-Type": "application/json"
                }
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                data = response.json()
                response_data = data.get("data", {})

                if not response_data: # Jika data kosong, artinya limit melebihi
                    self.show_message(
                        "Limited Access!",
                        "Anda melebihi batas limit, limit hanya 5 untuk pengguna guest.\n"
                        "Kunjungi goremote.id untuk dapatkan limit data tanpa batas!",
                        QMessageBox.Information
                    )
                    webbrowser.open("https://goremote.id/leads-generator/")
                    return
                else:
                    scraper = scrapping(self.ui)
                    scraper.run_scrapping(bisnis_segmentasi, geolokasi, request_quota, delay_pencarian, None)

            # Jika UUID ditemukan, ambil datanya
            # Cek apakah response JSON memiliki data
            if user_data and isinstance(user_data, dict):
                max_limit = user_data.get('max_limit', 0)
                used_limit = user_data.get('used_limit', 0)
            else:
                print("Warning: Data user tidak ditemukan atau format tidak sesuai.")
                max_limit = 5
                used_limit = 0


            limit_akhir = used_limit + int(request_quota)

            # Cek apakah masih bisa request data
            if limit_akhir > max_limit:
                self.show_message(
                    "Limited Access!",
                    "Anda sedang menggunakan Trial Package (Max 5 Data).\n"
                    "Kunjungi goremote.id untuk dapatkan limit data tanpa batas!",
                    QMessageBox.Information
                )
                webbrowser.open("https://goremote.id/leads-generator/")
            else:
                scraper = scrapping(self.ui)
                scraper.run_scrapping(bisnis_segmentasi, geolokasi, request_quota, delay_pencarian, None)

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Unexpected Error: {err}")


    def update_limit_guest(self, used_limit):
        os = self.uuidos.get_os_name()
        arsitektur = self.uuidos.get_architecture()
        uuid = self.uuidos.get_uuid()
        url = f"{self.URLAPI}/guest-request"
        try:
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "uuid_os": uuid,
                "os_name": os,
                "arch_os": arsitektur,
                "used_limit": used_limit
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Unexpected Error: {err}")

    def sisa_quota(self, token):
        url = f"{self.URLAPI}/quota"
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            quota_saat_ini = data['data']['sisa_quota']
            return quota_saat_ini
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Unexpected Error: {err}")





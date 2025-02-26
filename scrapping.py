# This Python file uses the following encoding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from databasesqlite import databasesqlite
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from itertools import zip_longest
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QMetaObject, Qt, QObject, Slot, Signal
from tablehelper import TableHelper
import requests
import time
import threading
import re
import subprocess
import signal
import sys
import time
import os

class scrapping(QObject):
    update_table_terkini = Signal()
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.update_table_terkini.connect(self.test_signal)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode headless (opsional)
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.nama_lokasi = []
        self.results = []
        self.ratings = []
        self.jumlah_ulasan = []
        self.harga_items = []
        self.alamat_items = []
        self.website_items = []
        self.no_telpon_items = []
        self.link_items = []

        self.instagram_items = []
        self.twitter_items = []
        self.facebook_items = []
        self.linkedln_items = []
        self.tiktok_items = []
        self.youtube_items = []
        self.email_items = []
        self.search_date = 0
        self.bisnisSegmentasi = None
        self.geolokasiBisnis = None

    def run_scrapping(self, bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian, id_simpan_riwayat):
        self.ui.btnCancel.setEnabled(True)
        self.ui.btnSearch.setEnabled(False)
        self.ui.btnDownload.setEnabled(False)

        self.bisnisSegmentasi = bisnis_segmentasi
        self.geolokasiBisnis = geolokasi
        #Jalankan scrapping di thread terpisah agar GUI tidak not responding
        thread = threading.Thread(target=self._scrape, args=(bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian, id_simpan_riwayat))
        thread.start()

    def message_success(self):
        # Panggil _show_message di UI thread dengan benar
        QMetaObject.invokeMethod(self, "_show_message", Qt.QueuedConnection)

    @Slot()
    def _show_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Success")
        msg.setText("Pencarian data berhasil dilakukan")
        msg.setStyleSheet("QLabel { color : white; } QPushButton { color : black; }")
        msg.exec()

    def is_website_alive(self, url):
        """Cek apakah website masih aktif atau tidak."""
        try:
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


    def _scrape(self, bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian, id_simpan_riwayat):
        url_pencarian = f"https://www.google.com/maps/search/{bisnis_segmentasi}+di+{geolokasi}"

        # Buka halaman pencarian
        self.driver.get(url_pencarian)
        time.sleep(2)

        # Proses scrapping
        self.search_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.scrapping_process(self.driver, int(limit_pencarian), int(delay_pencarian), id_simpan_riwayat)

        print("Scrapping selesai.")
        self.driver.quit()
        self.message_success()
        self.update_table()
        self.ui.btnCancel.setEnabled(False)
        self.ui.btnSearch.setEnabled(True)
        self.ui.btnDownload.setEnabled(True)

        self.ui.progressBar.setValue(0)


    def update_table(self):
        db = databasesqlite()
        results_current = db.get_current_result()
        results_history = db.get_search_history()
        TableHelper.populate_table(self.ui.tableTerkini, results_current)
        TableHelper.populate_table(self.ui.tableRiwayatPencarian, results_history)


    def scrapping_process(self, driver, limit, delay, id_simpan_riwayat):
        db = databasesqlite()
        el_nama_lokasi = self.driver.find_elements("xpath", f"//*[contains(@class, 'hfpxzc')]")
        el_rating = self.driver.find_elements("css selector", f".MW4etd") or []  # Pastikan selalu ada
        el_ulasan = self.driver.find_elements("css selector", f".UY7F9") or []  # Pastikan selalu ada
        previous_length = len(el_nama_lokasi)

        time.sleep(3)  # Beri waktu agar elemen pertama muncul

        while len(el_nama_lokasi) < limit:

            last_element = el_nama_lokasi[-1] if el_nama_lokasi else None
            if last_element:
                 self.driver.execute_script("arguments[0].scrollIntoView(true);", last_element)

            time.sleep(delay)

            el_nama_lokasi = self.driver.find_elements("xpath", f"//*[contains(@class, 'hfpxzc')]")
            el_rating = self.driver.find_elements("css selector", f".MW4etd") or []  # Pastikan selalu ada
            el_ulasan = self.driver.find_elements("css selector", f".UY7F9") or []  # Pastikan selalu ada

            if len(el_nama_lokasi) == previous_length:
                print("Jumlah elemen tidak bertambah, keluar dari loop.")
                break

            if len(el_nama_lokasi) >= limit:
                break

            previous_length = len(el_nama_lokasi)

        # Pastikan daftar ada, meskipun kosong
        el_rating = el_rating if el_rating else ["N/A"] * len(el_nama_lokasi)
        el_ulasan = el_ulasan if el_ulasan else ["N/A"] * len(el_nama_lokasi)

        # inisaliasasi progress bar
        total_lokasi = min(limit, len(el_nama_lokasi))  # Batas lokasi yang akan di-scrape
        total_website = len(self.website_items)  # Jumlah website yang ditemukan untuk dikunjungi
        total_steps = total_lokasi * 3 + total_website  # Semua langkah yang harus diselesaikan
        progress_counter = 0  # Inisialisasi progress

        for i in range(min(limit, len(el_nama_lokasi))):
            nama = el_nama_lokasi[i].get_attribute("aria-label") if i < len(el_nama_lokasi) else "N/A"
            rating = el_rating[i].text if i < len(el_rating) else "N/A"
            ulasan = el_ulasan[i].text if i < len(el_ulasan) else "N/A"

            link = el_nama_lokasi[i].get_attribute("href") if i < len(el_nama_lokasi) else "N/A"
            self.link_items.append(link)
            self.nama_lokasi.append(nama)
            print(f"{i+1}. {nama} | Rating: {rating} | Ulasan: {ulasan} | Link: {link}")
            progress_counter += 1
            progress = (progress_counter / total_steps) * 100
            self.ui.progressBar.setValue(progress)
            QApplication.processEvents()  # Agar UI tetap responsif


        for link in self.link_items:
            try:
                print("navigasi ke : {} ".format(link))
                self.driver.get(link)
                time.sleep(delay)
                wait = WebDriverWait(self.driver, 10)

                address_text = None
                phone_number = None
                website_official = None
                instagram_official = None
                facebook_official = None
                tiktok_official = None
                youtube_official = None
                linkedln_official = None
                email_official = None
                twitter_official = None

                try:
                    # Cari tombol alamat
                    address_button = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, f"button[data-item-id='address'"))
                    )
                    address_text = address_button.get_attribute("aria-label").replace("Alamat: ", "").strip()
                except Exception:
                    print("Alamat tidak ditemukan di halaman ini")

                try:
                    # Cari tombol nomor telepon
                    phone_button = self.driver.find_element(By.CSS_SELECTOR, f"button[data-item-id*='phone']")
                    phone_number = phone_button.get_attribute("aria-label").replace("Telepon: ", "").strip()
                except Exception:
                    print("Nomor telepon tidak ditemukan di halaman ini")

                try:
                    # Cari tombol website resmi
                    website_official_button = self.driver.find_element(By.CSS_SELECTOR, f"a[data-item-id*='authority']")
                    website_official = website_official_button.get_attribute("href")
                except Exception:
                    website_official = "not found"
                    print(f"Website tidak ditemukan di halaman ini: {website_official}")

                # Simpan hasil scraping
                self.alamat_items.append(address_text)
                self.no_telpon_items.append(phone_number)
                self.website_items.append(website_official)
                progress_counter += 1
                progress = (progress_counter / total_steps) * 100
                self.ui.progressBar.setValue(progress)
                QApplication.processEvents()

            except Exception as e:
                print(f"Error navigating to {link}: {e}")

            self.driver.back()
            time.sleep(delay)

        # Cari elemen rating
        elements_with_class = self.driver.find_elements(By.CSS_SELECTOR, f".MW4etd")
        for element in elements_with_class:
            if element.is_displayed():  # Ambil teks hanya jika elemen terlihat
                self.ratings.append(element.text)

        # Cari elemen ulasan
        elements_with_class = self.driver.find_elements(By.CSS_SELECTOR, f".UY7F9")
        for element in elements_with_class:
            if element.is_displayed():  # Ambil teks hanya jika elemen terlihat
                self.jumlah_ulasan.append(element.text.replace("(", "").replace(")", ""))  # Hapus tanda kurung

        for url in self.website_items:
            sosmed_results = {
                "instagram": "",
                "facebook": "",
                "twitter": "",
                "tiktok": "",
                "youtube": "",
                "linkedin": "",
            }
            email_official = ""

            if url == "not found":
                print("Tidak ada website yang ditemukan")
            else:
                if not self.is_website_alive(url):
                    print(f"Website {url} tidak aktif, melewati...")
                    continue

                try:
                    self.driver.get(url)
                    print(f"Masuk ke dalam website resmi: {url}")

                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                    except TimeoutException:
                        print(f"Website {url} terlalu lama loading, melewati...")
                        continue

                    # Pencarian Sosial Media
                    social_media_links = {
                        "instagram": "a[href*='instagram']",
                        "facebook": "a[href*='facebook']",
                        "twitter": "a[href*='twitter'], a[href*='x.com']",
                        "tiktok": "a[href*='tiktok.com']",
                        "youtube": "a[href*='youtube.com/channel']",
                        "linkedin": "a[href*='linkedin.com']",
                    }

                    for key, selector in social_media_links.items():
                        try:
                            button = self.driver.find_element(By.CSS_SELECTOR, selector)
                            link = button.get_attribute("href")
                            if link:
                                sosmed_results[key] = link
                                print(f"{key.capitalize()} ditemukan: {link}")
                        except (NoSuchElementException, TimeoutException):
                            print(f"{key.capitalize()} tidak ditemukan di halaman website resmi")

                    # Cari Email
                    try:
                        emails_found = set()
                        email_xpath = "//a[starts-with(@href, 'mailto:')] | //p[contains(text(), '@')] | //span[contains(text(), '@')] | //div[contains(text(), '@')]"
                        email_elements = self.driver.find_elements(By.XPATH, email_xpath)

                        for element in email_elements:
                            text = element.get_attribute("href") or element.text
                            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))
                            emails_found.update(emails)

                        email_official = ", ".join(emails_found) if emails_found else ""
                        if email_official:
                            print(f"Email ditemukan: {email_official}")
                        else:
                            print("Email tidak ditemukan")

                    except Exception as e:
                        print(f"Terjadi kesalahan saat mencari email: {e}")

                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Terjadi error saat memproses {url}: {e}")
                    continue

                self.driver.back()  # Hanya kembali jika website aktif
            # Simpan hasil ke dalam list
            self.instagram_items.append(sosmed_results["instagram"])
            self.facebook_items.append(sosmed_results["facebook"])
            self.twitter_items.append(sosmed_results["twitter"])
            self.tiktok_items.append(sosmed_results["tiktok"])
            self.youtube_items.append(sosmed_results["youtube"])
            self.linkedln_items.append(sosmed_results["linkedin"])
            self.email_items.append(email_official)


            progress_counter += 1
            progress = (progress_counter / total_steps) * 100
            self.ui.progressBar.setValue(progress)
            QApplication.processEvents()

        self.driver.quit()
        for label, rating, ulasan, harga, alamat, website, no_telpon, link, instagram, facebook, twitter, youtube, email, linkedln, tiktok in zip_longest(
                self.nama_lokasi, self.ratings, self.jumlah_ulasan, self.harga_items, self.alamat_items, self.website_items,
                self.no_telpon_items, self.link_items, self.instagram_items, self.facebook_items,
                self.twitter_items, self.youtube_items, self.email_items, self.linkedln_items, self.tiktok_items, fillvalue=""):

            self.results.append({
                "nama_lokasi": label,
                "rate": rating,
                "jumlah_ulasan": ulasan,
                "harga": harga,
                "alamat": alamat,
                "website": website,
                "no_telepon": no_telpon,
                "link": link,
                "instagram": instagram,
                "twitter": twitter,
                "tiktok": tiktok,
                "linkedln": linkedln,
                "youtube": youtube,
                "facebook": facebook,
                "email": email
            })

        jumlah_valid_results = sum(1 for result in self.results if result.get("nama_lokasi"))
        #simpan riwayat pencarian db lokal
        db.save_search_history(self.bisnisSegmentasi, self.geolokasiBisnis, int(limit), int(delay), jumlah_valid_results, self.search_date, self.results)
        #simpan riwayat pencarian ke api
        if id_simpan_riwayat:
            from api import API
            api_instance = API(self.ui)
            api_instance.simpan_riwayat_pencarian(jumlah_valid_results, id_simpan_riwayat)

            is_login = db.get_session()
            token_login = is_login[0]
            sisa = api_instance.sisa_quota(token_login)
            self.ui.lblSisaKuota.setText(str(sisa))
        else:
            from api import API
            api_instance = API(self.ui)
            api_instance.update_limit_guest(jumlah_valid_results)

    def cancel(self):
        """Menutup Selenium dan memastikan ChromeDriver benar-benar berhenti di Windows, Linux, atau macOS."""
        if self.driver:
            try:
                self.driver.quit()  # Tutup browser Selenium
                self.driver = None  # Hapus referensi driver
            except Exception as e:
                print(f"Error saat menutup Selenium: {e}")

        # Tunggu sebentar untuk memastikan driver berhenti
        time.sleep(1)

        # Deteksi OS dan gunakan perintah yang sesuai
        if sys.platform.startswith("win"):  # Windows
            try:
                subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("ChromeDriver berhasil dihentikan di Windows.")
            except Exception as e:
                print(f"Error saat mematikan ChromeDriver di Windows: {e}")

        else:  # Linux / macOS
            try:
                subprocess.run(["pkill", "-f", "chromedriver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("ChromeDriver berhasil dihentikan di Linux/macOS.")
            except Exception as e:
                print(f"Error saat mematikan ChromeDriver di Linux/macOS: {e}")

        # Reset UI
        self.ui.progressBar.setValue(0)
        self.ui.btnCancel.setEnabled(False)
        self.ui.btnSearch.setEnabled(True)
        self.ui.btnDownload.setEnabled(True)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Cancel")
        msg.setText("Pencarian data dibatalkan")
        msg.setStyleSheet("QLabel { color : white; } QPushButton { color : black; }")
        msg.exec()

    def test_signal(self):
        print("✅ test_signal() terpanggil dari scrapping!")

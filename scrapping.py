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
import time
import threading
import re
import json


class scrapping:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Mode headless (opsional)
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

    def run_scrapping(self, bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian):
        #Jalankan scrapping di thread terpisah agar GUI tidak not responding
        thread = threading.Thread(target=self._scrape, args=(bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian))
        thread.start()

    def _scrape(self, bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian):
        db = databasesqlite()
        url_pencarian = f"https://www.google.com/maps/search/{bisnis_segmentasi}+di+{geolokasi}"

        # Buka halaman pencarian
        self.driver.get(url_pencarian)
        time.sleep(2)

        # Proses scrapping
        search_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.scrapping_process(self.driver, int(limit_pencarian), int(delay_pencarian))

        #simpan riwayat pencarian
        db.save_search_history(bisnis_segmentasi, geolokasi, int(limit_pencarian), int(delay_pencarian), search_date)

        print("Scrapping selesai.")
        self.driver.quit()

    def scrapping_process(self, driver, limit, delay):
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

        for i in range(min(limit, len(el_nama_lokasi))):
            nama = el_nama_lokasi[i].get_attribute("aria-label") if i < len(el_nama_lokasi) else "N/A"
            rating = el_rating[i].text if i < len(el_rating) else "N/A"
            ulasan = el_ulasan[i].text if i < len(el_ulasan) else "N/A"

            link = el_nama_lokasi[i].get_attribute("href") if i < len(el_nama_lokasi) else "N/A"
            self.link_items.append(link)
            self.nama_lokasi.append(nama)
            print(f"{i+1}. {nama} | Rating: {rating} | Ulasan: {ulasan} | Link: {link}")


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
            if url == "not found":
                print("Tidak ada website yang ditemukan")
                instagram_official = ""
                facebook_official = ""
                twitter_official = ""
                tiktok_official = ""
                youtube_official = ""
                linkedln_official = ""
                email_official = ""
            else:
                try:
                    self.driver.get(url)
                    print(f"Masuk ke dalam website resmi: {url}")

                    # Cari Instagram
                    try:
                        instagram_button = self.driver.find_element(By.CSS_SELECTOR, f"a[href*='instagram']")
                        instagram_official = instagram_button.get_attribute("href")
                        print(f"Instagram ditemukan: {instagram_official}")
                    except (NoSuchElementException, TimeoutException):
                        print("Instagram tidak ditemukan di halaman website resmi")

                    # Cari Facebook
                    try:
                        facebook_button = self.driver.find_element(By.CSS_SELECTOR, f"a[href*='facebook']")
                        facebook_official = facebook_button.get_attribute("href")
                        print(f"Facebook ditemukan: {facebook_official}")
                    except (NoSuchElementException, TimeoutException):
                        print("Facebook tidak ditemukan di halaman website resmi")

                    # Cari Twitter
                    try:
                        twitter_button = self.driver.find_element(By.CSS_SELECTOR, 'a[href*="twitter"], a[href*="x.com"]')
                        twitter_official = twitter_button.get_attribute("href")
                        print(f"Twitter ditemukan: {twitter_official}")
                    except (NoSuchElementException, TimeoutException):
                        print("Twitter tidak ditemukan di halaman website resmi")

                    # Cari TikTok
                    try:
                        tiktok_button = self.driver.find_element(By.CSS_SELECTOR, f"a[href*='tiktok.com']")
                        tiktok_official = tiktok_button.get_attribute("href")
                        print(f"TikTok ditemukan: {tiktok_official}")
                    except (NoSuchElementException, TimeoutException):
                        print("TikTok tidak ditemukan di halaman website resmi")

                    # Cari LinkedIn
                    try:
                        linkedin_button = self.driver.find_element(By.CSS_SELECTOR, f"a[href*='linkedin.com']")
                        linkedin_official = linkedin_button.get_attribute("href")
                        print(f"LinkedIn ditemukan: {linkedin_official}")
                    except (NoSuchElementException, TimeoutException):
                        print("LinkedIn tidak ditemukan di halaman website resmi")

                    # Cari YouTube
                    try:
                        youtube_button = self.driver.find_element(By.CSS_SELECTOR, 'a[href*="youtube.com/channel"]')
                        youtube_official = youtube_button.get_attribute("href")
                        print(f"YouTube ditemukan: {youtube_official}")
                    except (NoSuchElementException, TimeoutException):
                        print("YouTube tidak ditemukan di halaman website resmi")

                    # Cari email
                    try:
                        emails_found = set()
                        email_xpath = "//a[starts-with(@href, 'mailto:')] | //p[contains(text(), '@')] | //span[contains(text(), '@')] | //div[contains(text(), '@')]"
                        email_elements = self.driver.find_elements(By.XPATH, email_xpath)

                        for element in email_elements:
                            text = element.get_attribute("href") or element.text
                            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))
                            emails_found.update(emails)

                            email_official = ", ".join(emails_found) if emails_found else None
                            if email_official:
                                print(f"Email ditemukan: {email_official}")
                            else:
                                print("Email tidak ditemukan")

                    except Exception as e:
                                print(f"Terjadi kesalahan saat mencari email: {e}")

                except (TimeoutException, NoSuchElementException) as e:
                    print(f"Terjadi error saat memproses {url}: {e}")
                    continue

                self.driver.back()

                # Simpan hasil
                self.instagram_items.append(instagram_official)
                self.facebook_items.append(facebook_official)
                self.twitter_items.append(twitter_official)
                self.tiktok_items.append(tiktok_official)
                self.youtube_items.append(youtube_official)
                self.linkedln_items.append(linkedln_official)
                self.email_items.append(email_official)

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
        with open("results.txt", "w", encoding="utf-8") as file:
            json.dump(self.results, file, indent=4, ensure_ascii=False)

        print("Data berhasil disimpan dalam results.txt")


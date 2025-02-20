# This Python file uses the following encoding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading

class scrapping:
    def __init__(self):
        self.results = []  # Menyimpan hasil scrapping

    def run_scrapping(self, bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian):
        #Jalankan scrapping di thread terpisah agar GUI tidak not responding
        thread = threading.Thread(target=self._scrape, args=(bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian))
        thread.start()

    def _scrape(self, bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian):
        url_pencarian = f"https://www.google.com/maps/search/{bisnis_segmentasi}+di+{geolokasi}"

        # Setting Chrome Driver
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Mode headless (Opsional)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Buka halaman pencarian
        driver.get(url_pencarian)
        time.sleep(2)

        # Proses scrapping
        self.scrapping_process(driver, int(limit_pencarian), int(delay_pencarian))

        print("Scrapping selesai.")
        driver.quit()

    def scrapping_process(self, driver, limit, delay):
        el_nama_lokasi = driver.find_elements("xpath", f"//*[contains(@class, 'hfpxzc')]")
        el_rating = driver.find_elements("css selector", f".MW4etd") or []  # Pastikan selalu ada
        el_ulasan = driver.find_elements("css selector", f".UY7F9") or []  # Pastikan selalu ada
        nama_lokasi = []
        link_internal_maps = []
        previous_length = len(el_nama_lokasi)

        time.sleep(3)  # Beri waktu agar elemen pertama muncul

        while len(el_nama_lokasi) < limit:
            last_element = el_nama_lokasi[-1] if el_nama_lokasi else None
            if last_element:
                 driver.execute_script("arguments[0].scrollIntoView(true);", last_element)

            time.sleep(delay)

            el_nama_lokasi = driver.find_elements("xpath", f"//*[contains(@class, 'hfpxzc')]")
            el_rating = driver.find_elements("css selector", f".MW4etd") or []  # Pastikan selalu ada
            el_ulasan = driver.find_elements("css selector", f".UY7F9") or []  # Pastikan selalu ada

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
            link_internal_maps.append(link)

            print(f"{i+1}. {nama} | Rating: {rating} | Ulasan: {ulasan} | Link: {link}")

        driver.quit()

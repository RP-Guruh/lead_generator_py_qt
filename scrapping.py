# This Python file uses the following encoding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class scrapping:
    def __init__(self):
        pass

    def run_scrapping(bisnis_segmentasi, geolokasi, limit_pencarian, delay_pencarian):
        # url pencarian
        url_pencarian = "https://www.google.com/maps/search/{}+di+{}".format(bisnis_segmentasi, geolokasi)
        # setting chrome driver path
        # menggunakan chrome untuk menjalankan selenium
        driver_path = "./chromedriver/chromedriver"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)

        #buka chrome
        driver.get(url_pencarian)


        print("bisnis segmentasi : {} \n".format(bisnis_segmentasi))
        print("geolokasi : {} \n".format(geolokasi))
        print("limit pencarian : {} \n".format(limit_pencarian))
        print("delay pencarian : {} \n".format(delay_pencarian))

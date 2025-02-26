import logging
import os

class Logger:
    def __init__(self, log_file='logging.log'):
        self.log_file = log_file

        # Cek apakah file log sudah ada, jika tidak buat
        if not os.path.exists(self.log_file):
            open(self.log_file, 'w').close()  # Buat file kosong

        # Ambil instance logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Cegah duplikasi handler jika logger sudah dikonfigurasi sebelumnya
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def write_logging(self, message):
        self.logger.debug(message)  # Menulis log sebagai DEBUG

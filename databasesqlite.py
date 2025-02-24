from PySide6.QtCore import Signal, QObject
import sqlite3
import os

class databasesqlite(QObject):
    dataInserted = Signal()

    def __init__(self):
        super().__init__()
        self.db_file = "leadgenerator.db"
        self.conn = None
        self.connect_db()

    def connect_db(self):
        db_exists = os.path.exists(self.db_file)
        if not db_exists:
            print(f"Database {self.db_file} tidak ditemukan. Membuat database baru...")

        self.conn = sqlite3.connect(self.db_file)
        if not db_exists:
            self.build_table()  # Hanya buat tabel jika DB baru dibuat
            print("Tabel berhasil dibuat.")

    def build_table(self):
        cursor = self.conn.cursor()

        # Buat tabel search_histories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_histories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                place TEXT,
                search_limit TEXT,
                delay TEXT,
                hasil TEXT,
                search_date TEXT
            )
        ''')
        print("Membuat table search_histories")

        # Buat tabel search_results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_histories INTEGER,
                nama_lokasi TEXT,
                rate TEXT,
                jumlah_ulasan TEXT,
                alamat TEXT,
                website TEXT,
                no_telepon TEXT,
                link TEXT,
                twitter TEXT,
                tiktok TEXT,
                instagram TEXT,
                facebook TEXT,
                youtube TEXT,
                linkedln TEXT,
                email TEXT
            )
        ''')
        print("Membuat table search_results")

        # Buat tabel session_login
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_login (
                id_user INTEGER,
                token TEXT,
                name TEXT,
                email TEXT,
                is_login TEXT
            )
        ''')
        print("Membuat table session_login")

        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            print("Koneksi database ditutup.")

    def get_cursor(self):
        return self.conn.cursor()

    def get_connection(self):
        return self.conn

    def save_search_history(self, keyword, place, search_limit, delay, hasil, search_date, results_search):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO search_histories (keyword, place, search_limit, delay, hasil, search_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (keyword, place, search_limit, delay, hasil, search_date))

            self.conn.commit()

            # Ambil ID terakhir yang baru saja dimasukkan
            last_id = cursor.lastrowid

            data_to_insert = [
                (
                    last_id,
                    result['nama_lokasi'], result['rate'], result['jumlah_ulasan'], result['alamat'],
                    result['website'], result['no_telepon'], result['link'],
                    result['twitter'], result['tiktok'], result['instagram'], result['facebook'],
                    result['youtube'], result['linkedln'], result['email']
                )
                for result in results_search if result['nama_lokasi']
            ]

            cursor.executemany('''
                INSERT INTO search_results (id_histories, nama_lokasi, rate, jumlah_ulasan, alamat, website, no_telepon, link,
                                              twitter, tiktok, instagram, facebook, youtube, linkedln, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data_to_insert)

            self.conn.commit()

            # Emit signal setelah data berhasil disimpan
            self.dataInserted.emit()

            print("Riwayat pencarian berhasil disimpan.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat menyimpan riwayat pencarian: {e}")


    def get_current_result(self):
        try:
            cursor = self.conn.cursor()

            # Ambil last_id dari search_histories
            cursor.execute('SELECT MAX(id) FROM search_histories')
            last_id = cursor.fetchone()[0]

            if last_id is None:
                return []  # Jika tidak ada data, kembalikan list kosong

            # Ambil data berdasarkan id_histories
            cursor.execute('SELECT nama_lokasi, rate, jumlah_ulasan, no_telepon, email, website, alamat, instagram, facebook, twitter, linkedln, youtube, tiktok, link FROM search_results WHERE id_histories = ?', (last_id,))
            rows = cursor.fetchall()

            return rows  # Kembalikan hasilnya

        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat mengambil data hasil: {e}")
            return []

    def get_search_history(self):
        try:
            cursor = self.conn.cursor()

            # Ambil data berdasarkan id_histories
            cursor.execute('SELECT id, keyword, place, search_limit, hasil, delay, search_date FROM search_histories ORDER BY id DESC')
            rows = cursor.fetchall()

            return rows  # Kembalikan hasilnya

        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat mengambil data hasil: {e}")
            return []

    def get_data_byid(self, id):
        try:
            cursor = self.conn.cursor()
            # Ambil data berdasarkan id_histories
            cursor.execute('SELECT nama_lokasi, rate, jumlah_ulasan, no_telepon, email, website, alamat, instagram, facebook, twitter, linkedln, youtube, tiktok, link FROM search_results WHERE id_histories = ?', (id,))
            rows = cursor.fetchall()

            return rows  # Kembalikan hasilnya

        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat mengambil data hasil: {e}")
            return []


import sqlite3
import os

class databasesqlite:
    def __init__(self):
        self.db_file = "leadgenerator.db"
        self.conn = None
        self.connect()

    def connect(self):
        db_exists = os.path.exists(self.db_file)
        if not db_exists:
            print(f"Database {self.db_file} tidak ditemukan. Membuat database baru...")

        self.conn = sqlite3.connect(self.db_file)
        if not db_exists:
            self.build_table()
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
                harga TEXT,
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

    def save_search_history(self, keyword, place, search_limit, delay, search_date):

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO search_histories (keyword, place, search_limit, delay, search_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (keyword, place, search_limit, delay, search_date))

            self.conn.commit()
            print("Riwayat pencarian berhasil disimpan.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat menyimpan riwayat pencarian: {e}")

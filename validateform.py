class validateform:
    def __init__(self):
        pass

    @staticmethod
    def validate_form(bisnis_val, geolokasi_val, limit_val, delay_val):

        if not bisnis_val:
            pesan = "Bisnis segmentasi tidak boleh kosong"
            return False, pesan

        if not geolokasi_val:
            pesan = "Geolokasi tidak boleh kosong"
            return False, pesan

        if not limit_val:
            pesan = "Limit tidak boleh kosong"
            return False, pesan
        try:
            limit_val = int(limit_val)
            if limit_val <= 0:
                pesan = "Limit harus lebih besar dari 0"
                return False, pesan
        except ValueError:
            pesan = "Limit harus berupa angka"
            return False, pesan

        if not delay_val:
            pesan = "Delay tidak boleh kosong"
            return False, pesan
        try:
            delay_val = int(delay_val)
            if delay_val <= 0:
                pesan = "Delay harus lebih besar dari 0"
                return False, pesan
        except ValueError:
            pesan = "Delay harus berupa angka"
            return False, pesan

        return True, "Validasi berhasil!"

    def validate_login_form(email, password):
        if not email:
            pesan = "Email tidak boleh kosong"
            return False, pesan

        if not password:
            pesan = "Password tidak boleh kosong"
            return False, pesan

        return True, "Validasi berhasil!"

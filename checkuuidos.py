import uuid
import platform

class checkuuidos:
    @staticmethod
    def get_os_name():
        """Mendapatkan nama sistem operasi."""
        return platform.system()

    @staticmethod
    def get_architecture():
        """Mendapatkan arsitektur sistem (32-bit / 64-bit)."""
        return platform.architecture()[0]

    @staticmethod
    def get_uuid():
        """Mendapatkan UUID perangkat sesuai OS."""
        os_name = checkuuidos.get_os_name()

        if os_name == "Windows":
            return str(uuid.UUID(int=uuid.getnode()))
        elif os_name in ["Linux", "Darwin"]:  # Darwin untuk macOS
            try:
                with open('/etc/machine-id', 'r') as file:
                    return file.read().strip()
            except FileNotFoundError:
                with open('/var/lib/dbus/machine-id', 'r') as file:
                    return file.read().strip()
        else:
            return "OS tidak dikenali"

# Contoh penggunaan
# os_name = CheckUUIDOS.get_os_name()
# architecture = CheckUUIDOS.get_architecture()
# uuid_str = CheckUUIDOS.get_uuid()

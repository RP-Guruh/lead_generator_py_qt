import uuid
import platform

class checkuuidos:
    def __init__(self):
        pass

    @staticmethod
    def generate_uuid():
        os_name = platform.system()

        if os_name == "Windows":
            # Mendapatkan UUID di Windows
            return str(uuid.UUID(int=uuid.getnode()))
        elif os_name == "Linux" or os_name == "Darwin":  # Darwin untuk macOS
            # Mendapatkan UUID di Linux atau macOS
            try:
                with open('/etc/machine-id', 'r') as file:
                    return file.read().strip()
            except FileNotFoundError:
                with open('/var/lib/dbus/machine-id', 'r') as file:
                    return file.read().strip()
        else:
            return "OS tidak dikenali"

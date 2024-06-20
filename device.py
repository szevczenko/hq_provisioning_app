import requests
from scan_devices import ScanDevices


class Device:
    def __init__(self, address):
        self.address = address
        self.session = requests.Session()
    
    def get_serial_number(self):
        r"""Get serial number from device

        Returns serial number if operation success. Otherwise return None.
        :rtype: str or None
        """
        url = f"http://{self.address}:8000/api/sn"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    
    def set_serial_number(self, serial_number: str):
        r"""Set serial number

        :param serial_number: Serial number.
        :rtype: bool
        """
        url = f"http://{self.address}:8000/api/sn"
        response = self.session.post(url, serial_number)
        if response.status_code == 200:
            return True
        else:
            return False
    
    def set_ota_address(self):
        url = f"http://{self.address}:8000/api/ota"
        response = self.session.post(url, "1")


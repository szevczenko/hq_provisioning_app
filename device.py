import requests
import serial
from scan_devices import ScanDevices
import time
import json


class Device:
    def __init__(self, address: str = None, com: str = None, mac: str = None):
        self.address = address
        self.com = com
        self.mac = mac

    def get_serial_number(self):
        r"""Get serial number from device

        Returns serial number if operation success. Otherwise return None.
        :rtype: str or None
        """
        with requests.Session() as session:
            url = f"http://{self.address}:8000/api/sn"
            response = session.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return None

    def set_serial_number(self, serial_number: str):
        r"""Set serial number

        :param serial_number: Serial number.
        :rtype: bool
        """
        with requests.Session() as session:
            url = f"http://{self.address}:8000/api/sn"
            response = session.post(url, serial_number)
            if response.status_code == 200:
                return True
            else:
                return False

    def set_ota_address(self, url_file: str):
        r"""Set ota address

        :param url_file: URL to file.
        :rtype: bool
        """
        with requests.Session() as session:
            url = f"http://{self.address}:8000/api/ota"
            response = session.post(url, url_file)
            if response.status_code == 200:
                return True
            else:
                return False

    def wifi_connect(self, ssid: str, password: str):
        r"""Connect to wifi AP

        :note: Should be set device COM port
        :param ssid: ssid of access point.
        :param password: password to AP.
        Returns True if operation success. Otherwise return False.
        :rtype: bool
        """
        if self.com is None:
            print("COM Port not set for device")
            return False
        with serial.Serial(self.com, 115200, timeout=10) as ser:
            ser.write(bytes(f"join {ssid} {password}\r\n", "utf-8"))
            timeout = time.time() + 15  # 5 minutes from now
            while True:
                line = ser.readline()
                msg = line.decode("utf-8")
                print(msg)
                if "ERROR" in msg:
                    print(msg)
                    return False
                elif "OK" in msg:
                    print(msg)
                    return True
                if time.time() > timeout:
                    break
            return False

    def get_mac_address(self):
        r"""Get mac address from device

        :note: Should be set device COM port
        Returns mac address if operation success. Otherwise return False.
        :rtype: str or None
        """
        if self.com is None:
            print("COM Port not set for device")
            return None
        with serial.Serial(self.com, 115200, timeout=10) as ser:
            ser.write(bytes(f"get_mac\r\n", "utf-8"))
            line = ser.readline()
            line = ser.readline()
            msg = line.decode("utf-8")
            return msg

    def get_ota_status(self):
        r"""Get ota status

        :note: Should be set device COM port
        Returns tuple. In the first place download percentage, second place - status.
        :rtype: tuple or None
        """
        if self.address is None:
            print("Not set ip address")
            return None
        with requests.Session() as session:
            url = f"http://{self.address}:8000/api/ota/state"
            response = session.get(url)
            if response.status_code == 200:
                json_object = json.loads(response.text)
                return (json_object["percentage"], json_object["state"])
            else:
                return None

    def restart_http(self):
        r"""Restart device using http command

        :note: Should be set ip address
        :rtype: bool
        """
        if self.address is None:
            print("Not set ip address")
            return None
        with requests.Session() as session:
            url = f"http://{self.address}:8000/api/restart"
            response = session.get(url)
            print(response.text)
            if response.status_code == 200:
                return True
            else:
                return False


if __name__ == "__main__":
    # devices = ScanDevices("Production", 3)
    # address = devices[0][0]
    address = "192.168.1.154"
    dev = Device(address, "COM6")
    # result = dev.wifi_connect("TP-Link_2AC1", "19681115")
    # print(result)

    # result = dev.set_serial_number("12314123")
    # print(result)

    result = dev.get_serial_number()
    print(result)
    result = dev.get_ota_status()
    print(result)
    result = dev.restart_http()
    print(result)

    # result = dev.get_mac_address()
    # print(result)

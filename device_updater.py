from device import *
from app_config import *
from scan_devices import ScanDevices
import http.server
import os
from threading import Thread
import signal
import sys


def start_http_server(httpd: http.server.HTTPServer, ota_image_dir: str):
    os.chdir(ota_image_dir)
    httpd.serve_forever()


def _thread_cb(self):
    while self.run_thread:
        self._scan_devices()
        for device in self.dev_list:
            if isinstance(device, Device):
                state = device.get_ota_status()
                match state[1]:
                    case "idle":
                        self.start_download(device)

                    case "download":
                        print(f"device {device.mac}: {state}")

                    case "error":
                        print(f"device {device.mac}: {state}")

                    case "finish":
                        print(f"device {device.mac}: {state}")
                        device.restart_http()


class DeviceUpdater:
    def __init__(self, path_to_bin: str, server_address: str):
        head_tail = os.path.split(path_to_bin)
        self.filename = head_tail[1]
        self.path = head_tail[0]
        self.dev_list = []
        self.server_address = server_address
        self.run_thread = True
        self.httpd = http.server.HTTPServer(
            (server_address, 8080), http.server.SimpleHTTPRequestHandler
        )
        self.httpd_thread = Thread(target=start_http_server, args=[self.httpd, self.path])
        self.httpd_thread.start()

    def _scan_devices(self):
        self.dev_list.clear()
        scan_result = ScanDevices(name="Production")
        for dev in scan_result:
            address = dev[0]
            mac = dev[2]
            find_device = False
            for device in self.dev_list:
                if device.mac == mac:
                    find_device = True
                    break
            if find_device == False:
                self.dev_list.append(Device(address, None, mac))

    def start_download(self, device: Device):
        msg = f"Enter serial number for {device.mac} or exit: "
        sn = input(msg)
        print(sn)

        if sn == "exit":
            self.stop()
            return None

        url = f"http://{self.server_address}:8080/{self.filename}"
        print(url)
        if device.set_serial_number(sn) == False:
            print("Failed set serial number")
            return None
    
        device.set_ota_address(url)

    def run(self):
        self.thread = Thread(target=_thread_cb, args=(self,))
        self.thread.start()

    def stop(self):
        self.httpd.shutdown()
        self.run_thread = False

    def wait_to_end(self):
        self.thread.join()


if __name__ == "__main__":
    updater = DeviceUpdater("C:/projekty/esp32_sterownik/build/sterownik.bin", "192.168.1.155")
    def signal_handler(signal, frame):
        print("You pressed Ctrl+C!")
        updater.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    updater.run()
    updater.wait_to_end()
    updater.stop()

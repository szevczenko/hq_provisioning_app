from device import *
from app_config import *
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("ssid", help="access point SSID", type=str, default=None, required=False)
parser.add_argument("password", help="access point SSID", type=str, default=None)
parser.add_argument("port", help="COM port", type=str, default=None)

args = parser.parse_args()

print(args.ssid)

# app_config = AppConfig()

# wifi_ap_ssid = app_config.get_param("wifi_ap_ssid")
# wifi_ap_password = app_config.get_param("wifi_ap_password")

import os
import json
from datetime import datetime


class AppConfig:

    DEFAULT_CONFIG_PATH = "config/defaultAppConfig.json"
    SAVE_CONFIG_PATH = "tmp/appConfig.json"
    MKDIR_PATH = os.getcwd()

    def __init__(self):
        if not os.path.exists("./tmp"):
            os.system("mkdir tmp")
        save_config_full_path = os.path.join(AppConfig.MKDIR_PATH, AppConfig.SAVE_CONFIG_PATH)
        if os.path.exists(save_config_full_path) == False:
            with open(
                os.path.join(AppConfig.MKDIR_PATH, AppConfig.DEFAULT_CONFIG_PATH)
            ) as readFile:
                self.default = json.load(readFile)
            with open(
                os.path.join(AppConfig.MKDIR_PATH, AppConfig.SAVE_CONFIG_PATH), "w"
            ) as writeFile:
                json.dump(self.default, writeFile)

        with open(os.path.join(AppConfig.MKDIR_PATH, AppConfig.SAVE_CONFIG_PATH)) as readFile:
            self.config = json.load(readFile)

    def save_config(self):
        with open(os.path.join(AppConfig.MKDIR_PATH, AppConfig.SAVE_CONFIG_PATH), "w") as writeFile:
            json.dump(self.config, writeFile)

    def get_param(self, inputParameter):
        return self.config[inputParameter]

    def set_param(self, inputParameter, value):
        tmp_parameter = {inputParameter, value}
        self.config[inputParameter] = value
        self.save_config()

    def get_location_config(self):
        return AppConfig.MKDIR_PATH

    def __str__(self):
        return str(self.config)


if __name__ == "__main__":
    config = AppConfig()
    config.set_param("mysql_address", 10)
    config.save_config()
    param1 = config.get_param("mysql_address")
    param2 = config.get_param("database_login")
    print(f"{param1}, {param2}")

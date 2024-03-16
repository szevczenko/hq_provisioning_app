import os
import json
from datetime import datetime


class AppConfig:
    
    DEFAULT_CONFIG_PATH = "config\\defaultAppConfig.json"
    SAVE_CONFIG_PATH = "tmp\\appConfig.json"
    MKDIR_PATH = os.getcwd()

    def __init__(self):
        if os.path.exists('./tmp'):
            print("sciezka istnieje")
        else :
                  
            os.system('mkdir tmp')
             
        
        if os.path.exists(os.path.join(AppConfig.MKDIR_PATH , AppConfig.SAVE_CONFIG_PATH)) ==False:
            print("plik app config nie istnieje")
            print(os.path.join(AppConfig.MKDIR_PATH ,AppConfig.DEFAULT_CONFIG_PATH))
            with open(os.path.join(AppConfig.MKDIR_PATH ,AppConfig.DEFAULT_CONFIG_PATH)) as readFile:
                  self.default = json.load(readFile)
            with open(os.path.join(AppConfig.MKDIR_PATH , AppConfig.SAVE_CONFIG_PATH), "w") as writeFile:
                 json.dump(self.default, writeFile)       

        

        with open(os.path.join(AppConfig.MKDIR_PATH ,AppConfig.SAVE_CONFIG_PATH)) as readFile:
             self.config = json.load(readFile)
             print(self.config)


             
    def saveConfig(self):
        with open(os.path.join(AppConfig.MKDIR_PATH , AppConfig.SAVE_CONFIG_PATH), "w") as writeFile:
                 json.dump(self.config, writeFile)


    def get_param(self , inputParametr ):
        return(self.config[inputParametr])
    
    def set_param(self , inputParametr , value):
        tmp_paramet = {inputParametr , value}
        self.config[inputParametr] = value
        self.saveConfig()
        

    def get_location_config(self):
        return AppConfig.MKDIR_PATH
    
    def __str__(self):
        return str(self.config)
    

test = AppConfig()
print(test.get_param("database_adres"))
test.set_param("database_adres", "127.1.1.0")

if __name__ == "__main__":
    print("Class app_config run here")
    





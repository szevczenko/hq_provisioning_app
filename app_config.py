import os
import json
from datetime import datetime


class AppConfig:
    
    def __init__(self):
        with open('defultConfig.json') as f:
            self.defluat = json.load(f)
            self.location_config = self.defluat['location_config'] + "\sample.json"

        if os.path.isfile(self.location_config):
                with open(self.location_config) as file_read:
                     self.config = json.load(file_read)
        else:
                tmpConfig = self.defluat
                tmpConfig.pop("location_config")
                now = datetime.now()
                tmpConfig['timeToCreate'] = str(now.strftime("%Y:%m:%d  %H:%M:%S"))

                with open(self.location_config, "w") as outfile:
                    json.dump(tmpConfig, outfile)

                with open(self.location_config) as file_read:
                     self.config = json.load(file_read)        
          

    def save_config(self):
        with open(self.location_config , "w") as outfile:
             json.dump(self.config, outfile)

    def get_param(self , inputParametr ):
        return(self.config[inputParametr])
    
    def set_param(self , inputParametr , value):
        tmp_paramet = {inputParametr , value}
        self.config[inputParametr] = value
        self.save_config()
        #print("run set_param inputParmetr - ", inputParametr , "  value - " , value )

    def get_location_config(self):
        return self.location_config
    
    




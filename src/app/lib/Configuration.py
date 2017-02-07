import os
import json

LOOTGAME_CONF_PATH = os.getenv('LOOTGAME_CONF_PATH', "../config/config.json")

class Configuration():
    
    def __init__(self):
        with open(LOOTGAME_CONF_PATH) as f:
            conf_dict = json.loads(f.read())
        self.databasepath = conf_dict["DB-PATH"]
        self.root = conf_dict["ROOT"]
        self.logpath = conf_dict["LOG-PATH"]
        self.tracking_active = conf_dict["TRACKING-ACTIVE"]
        self.tracking_code = conf_dict["TRACKING-CODE"]

    def get_DatabasePath(self):
        return self.databasepath
        
    def get_RootPath(self):
        return self.root
        
    def get_LoggingPath(self):
        return self.logpath
        
    def get_tracking_code(self):
        return self.tracking_code

    def is_tracking_active(self):
        return self.tracking_active

    def appendToBasePath(self, appending):
        while (appending.startswith('/')):
            appending = appending[1:]
        var = os.path.join(self.root, appending)
        return var

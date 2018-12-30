import json
import os

# Default Bot Config Informations
default = {
    "Bot-Data":
        {"Token": 'InsertYourTokenHere.XXXXXX.XXXXXXXXX-XXXXXXXXXXXX',
         "ClientID": 0000000000000000000,
         "Locale": 'en_US.utf8',
         "Bot-OwnerID": 0000000000000000000,
         "Bot-Guild": 0000000000000000000,
         "BotPrefix": "!",
         },
    "Twitter":
        {"Notifications": False,
         "Message": "",
         "Sended": False,
         "ConsumerAPIKey": "",
         "ConsumerAPISecret": "",
         "AccessToken": "",
         "AccessSecret": ""
         },
    "Twitch":
        {"TwitchToken": "",
         "TwitchChannelName": ""
         }
}

cfg = {}


def cfg_load():
    """Load the Config file for the Bot or create one if it doesnt exists"""
    if os.path.exists('config/cfg.json'):
        with open("config/cfg.json", 'r', encoding='utf-8') as config:
            cfg_temp = json.load(config)
            cfg.update(cfg_temp)
    
    else:
        with open("config/cfg.json", 'w+', encoding='utf-8') as conf:
            json.dump(default, conf)
            cfg.update(conf)


cfg_load()

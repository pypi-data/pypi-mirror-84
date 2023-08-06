import json
from urllib.request import urlopen

import subprocess
from pymongo import MongoClient


def start_config(code):
    """
    Load a configuration of robot and install dependencies
    """
    print ("Robot Config")

    json_url = urlopen("http://robot.mangotest.com/" + code + ".json")
    config = json.loads(json_url.read())  # <-- read from it
    name = config["name"]
    name = name.lower().replace(" ", "_")

    client = MongoClient("mongodb://localhost:27017")
    db = client[name]

    config_db = db.confg.find_one({"code": name})
    if not config_db:
        db.config.insert(config)

        for pack in config['packages']:
            subprocess.check_call(['pip3', 'install', pack["name"], '--force-reinstall'])

from pymongo import MongoClient
import importlib


def create_executor(robot_name, category):
    client = MongoClient("mongodb://localhost:27017")
    robot_name = robot_name.lower().replace(" ", "_")
    db = client[robot_name]
    config_db = db.config.find_one()

    packages = config_db["packages"]
    package = filter(lambda x: x["category"] == category, packages)[0]

    module = importlib.import_module(package["name"] + ".executor")
    class_ = getattr(module, package["class"])
    return class_()

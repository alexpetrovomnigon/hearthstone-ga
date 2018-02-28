import config
import json
import os

class Source:
    def __init__(self):
        return None
    def get_source_dir(self):
        return config.DATA_DIRECTORY
    def load_data(self):
        dir = self.get_source_dir()
        json_path = os.path.join(dir, "cards.json")
        with open(json_path) as json_data:
            d = json.load(json_data)
            return d
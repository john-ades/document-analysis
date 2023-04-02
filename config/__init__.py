import os

from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
IS_DEBUG = True
if os.getenv("env") in ["PROD", "PRODUCTION"]:
    # is in production
    pass
else:
    # is in debug
    current_directory = os.path.dirname(os.path.realpath(__file__))
    config_object.read(current_directory+ "/local/keys.ini")

class Config:
    @staticmethod
    def openai_key():
        return config_object.get("THIRD_PARTY_API_KEYS","openai")

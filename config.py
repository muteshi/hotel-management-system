import os
import json


with open('/etc/config.json') as config_file:
    config = json.load(config_file)


secret_key = config.get('SECRET_KEY')

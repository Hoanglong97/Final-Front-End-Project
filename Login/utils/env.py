import os
from configparser import ConfigParser
from pathlib import Path

cur_dir = os.path.dirname(os.path.realpath(__file__))
main_dir = os.path.dirname(cur_dir)
# Read config.ini file
config_object = ConfigParser()
config_object.read(os.path.join(main_dir, "config.ini"))

CUR_PATH = Path(main_dir)
# WORKING_PATH = (CUR_PATH / config_object["WORKING"].get("temp_dir", "resources")).resolve()
main_dir = main_dir + config_object["WORKING"].get("temp_dir", "resources")
WORKING_PATH = Path(main_dir).resolve()
WORKING_DIR = str(WORKING_PATH)

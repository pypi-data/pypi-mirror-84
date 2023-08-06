import os
from pathlib import Path


API_HOST = os.environ.get('SAVVIHUB_API_HOST', 'http://localhost:10000')
WEB_HOST = os.environ.get('SAVVIHUB_WEB_HOST', 'http://localhost:3000')

CUR_DIR = os.getcwd()
DEFAULT_SAVVI_DIR = os.path.join(str(Path.home()), '.savvihub')
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_SAVVI_DIR, 'config.yml')

DEFAULT_SAVVIHUBFILE_YAML = 'savvihubfile.yml'
INQUIRER_NAME_IMAGE = 'image'
INQUIRER_NAME_RESOURCE = 'resource'
INQUIRER_NAME_DATASET = 'dataset'
INQUIRER_NAME_DATASET_REF = 'dataset_ref'
INQUIRER_NAME_DATASET_MOUNT_PATH = 'dataset_mount_path'
INQUIRER_NAME_COMMAND = 'command'

import os
from os.path import expanduser

ENV_DIC_STORAGES_PATH_NAME = "WIBSES_DICT_STORAGES_PATH"
ENV_SCRIPT_STORAGE_PATH_NAME = "WIBSES_SCRIPT_STORAGE_PATH"


#ASCI generator configs
ASCI_ALPHABET = map(lambda x: chr(x), range(ord('a'), ord('z') + 1))
ALPHABET = map(lambda x: unichr(x), range(ord('a'), ord('z') + 1)) + \
    [u'\u015b', u'\u017c', u'\u017a', u'\u0107', u'\u0105', u'\u0119', u'\xf3', u'\u0142', u'\u0144']


APP_WORKING_DIR = os.path.dirname(__file__)
SCRIPT_FORMAT_CONFIG_FILE = os.path.join(os.path.join(APP_WORKING_DIR, "configs"), "script_format.cfg")


#default paths configs
DEFAULT_APP_DATA_DIR = os.path.join(expanduser("~"), 'wibses')
DEFAULT_PYDIC_APP_STORAGE_DIR = 'dict_storage'
DEFAULT_SCRIPTS_APP_STORAGE_DIR = 'scripts_storage'


#default constants config
JSON_INDENT = 0
PYDIC_WORDS_CACHE_SIZE = 1000000

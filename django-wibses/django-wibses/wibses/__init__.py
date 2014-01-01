#ASCI generator configs
ASCI_ALPHABET = map(lambda x: chr(x), range(ord('a'), ord('z') + 1))
ALPHABET = ASCI_ALPHABET + ['\xc5\x9b', '\xc4\x87', '\xc5\xbc', '\xc5\xba',
                            '\xc4\x85', '\xc4\x99', '\xc3\xb3', '\xc5\x82']

ENV_DIC_STORAGE_PATH_NAME = "PYDIC_STORAGE_PATH"
ENV_SCRIPT_STORAGE_PATH_NAME = "WIBSES_SCRIPT_STORAGE"

import os

PROJECT_DIR = os.path.dirname(__file__)

#default paths configs
DEFAULT_PYDIC_STORAGES = ['/home/ork/Study/Inzynierka/Projekt/dictionaries']
DEFAULT_SCRIPT_STORAGE = '/home/ork/scr_storage'

DEFAULT_SCRIPT_FORMAT_CONFIG_FILE = os.path.join(os.path.join(PROJECT_DIR, "configs"), "script_format.cfg")

#default constants config
JSON_INDENT = 2
PYDIC_WORDS_CACHE_SIZE = 100000
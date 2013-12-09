#ASCI generator configs
ASCI_GENERATOR_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ENV_DIC_STORAGE_PATH_NAME = "PYDIC_STORAGE_PATH"
ENV_SCRIPT_STORAGE_PATH_NAME = "WIBSES_SCRIPT_STORAGE"

import os

PROJECT_DIR = os.path.dirname(__file__)

#default paths configs
DEFAULT_PYDIC_STORAGES = ['/home/ork/Study/Inzynierka/Projekt/dictionaries']
# DEFAULT_SCRIPT_STORAGE = os.path.join(PROJECT_DIR, 'scripts')
DEFAULT_SCRIPT_STORAGE = '/home/ork/scr_storage'

#Configuration of dictionary manager and script storage manager
JSON_TEMPLATE_SCRIPT_FILENAME = os.path.join(os.path.join(PROJECT_DIR, "configs"), "empty_template.json")
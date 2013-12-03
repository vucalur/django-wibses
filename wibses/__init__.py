ENV_DIC_PATHS_NAME = "PYDIC_PATH"
ENV_DIC_STORAGE_PATH_NAME = "PYDIC_STORAGE_PATH"

ENV_SCRIPT_STORAGE_PATH_NAME = "WIBSES_SCRIPT_STORAGE"

import os
from wibses.data_store.script_api import ScriptUtils
from wibses.py_dict.dict_api import DictionaryUtils

#temporary configs
PROJECT_DIR = os.path.dirname(__file__)

PYDIC_STORAGES = ['/home/ork/Study/Inzynierka/Projekt/dictionaries']
SCRIPT_STORAGE = os.path.join(PROJECT_DIR, 'scripts')
JSON_TEMPLATE_SCRIPT_FILENAME = os.path.join(os.path.join(PROJECT_DIR, "configs"), "empty_template.json")


ScriptUtils.set_script_template_filename(JSON_TEMPLATE_SCRIPT_FILENAME)
ScriptUtils.set_scripts_storage_path(SCRIPT_STORAGE)
ScriptUtils.initialize_from_current_config()

DictionaryUtils.add_dictionary_storages_paths(PYDIC_STORAGES)
DictionaryUtils.initialize_from_current_config()

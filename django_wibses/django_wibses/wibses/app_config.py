import os

from . import ENV_DIC_STORAGES_PATH_NAME, DEFAULT_PYDIC_APP_STORAGE_DIR, \
    DEFAULT_SCRIPTS_APP_STORAGE_DIR, ENV_SCRIPT_STORAGE_PATH_NAME, DEFAULT_APP_DATA_DIR

from data_store.script_api import ScriptUtils
from utils import merge_into_path
from py_dict.dict_api import DictionaryUtils


def __create_app_data_tree():
    dict_storage_path = merge_into_path([DEFAULT_APP_DATA_DIR, DEFAULT_PYDIC_APP_STORAGE_DIR])
    scripts_storage_path = merge_into_path([DEFAULT_APP_DATA_DIR, DEFAULT_SCRIPTS_APP_STORAGE_DIR])

    dirs_to_create = [
        DEFAULT_APP_DATA_DIR,
        dict_storage_path,
        scripts_storage_path
    ]

    for d in dirs_to_create:
        if not os.path.exists(d):
            os.mkdir(d)

    return {
        "dictionary_storages": [dict_storage_path],
        "scripts_storage": scripts_storage_path
    }


def configure_app(dictionary_storages=None, scripts_storage=None, use_defaults=False):
    if use_defaults:
        default_configs = __create_app_data_tree()
        dictionary_storages = default_configs["dictionary_storages"]
        scripts_storage = default_configs["scripts_storage"]
    else:
        not_specified = []
        if dictionary_storages is None:
            try:
                dict_str = os.environ[ENV_DIC_STORAGES_PATH_NAME]
                dictionary_storages = dict_str.split(os.pathsep)
            except KeyError:
                not_specified.append(ENV_DIC_STORAGES_PATH_NAME)

        if scripts_storage is None:
            try:
                scripts_storage = os.environ[ENV_SCRIPT_STORAGE_PATH_NAME]
            except KeyError:
                not_specified.append(ENV_SCRIPT_STORAGE_PATH_NAME)

        if len(not_specified) > 0:
            raise Exception("Environment variables are not set %s" % str(not_specified))

    DictionaryUtils.add_dictionary_storages_paths(dictionary_storages)
    ScriptUtils.set_scripts_storage_path(scripts_storage)

    ScriptUtils.initialize()
    DictionaryUtils.initialize()
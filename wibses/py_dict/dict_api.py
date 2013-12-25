import os
import json

from pydic import PyDic
from ..utils import get_folder_containing_names, merge_into_path


class NotRegisteredDictionaryException(Exception):
    def __init__(self, dic_name):
        Exception.__init__(self, 'Dictionary ' + str(dic_name) + ' was not registered in manager')
        self._dic_name = dic_name

    def get_dic_name(self):
        return self._dic_name


class DictionaryManager:
    def __init__(self, dictionaries_storages_list):
        self._dictionaries_map = dict()
        for storage in dictionaries_storages_list:
            storage_list_dicts = get_folder_containing_names(storage, incl_dir_names=True)
            for dic_dir in storage_list_dicts:
                dic_dir = merge_into_path([storage, dic_dir])
                assert isinstance(dic_dir, str)
                dic_name = dic_dir.split(os.sep)[-1]
                try:
                    dic_instance = PyDic(dic_dir)
                    self._dictionaries_map[dic_name] = dic_instance
                except Exception as e:
                    print str(e)

    def get_tokens_for_word_form(self, form):
        result = [{'base': form, 'id': '-', 'type': 'quotation', 'dic': "-", 'forms': [form]}]

        result_tail = []
        for registered_dic in self._dictionaries_map.values():
            result_tail.extend(self.__get_tokens_from_dic(form, registered_dic))

        result_tail.sort(key=lambda x: x['base'])
        result.extend(result_tail)

        return json.dumps(result, indent=1)

    def __get_tokens_from_dic(self, form, dic_instance):

        def create_token_description(token_pydic_id):
            token_id = str(token_pydic_id)
            base_form = dic_instance.id_base(token_id)
            forms = dic_instance.id_forms(token_id)
            return {'dic': dic_instance.name, 'id': token_id, 'base': base_form, 'forms': forms, 'type': "token"}

        possible_words = dic_instance.words_for_prefix(form)
        token_ids = set([])

        for word in possible_words:
            pydic_ids = dic_instance.id(word)
            if len(pydic_ids) > 0:
                #TODO taipsedog: maybe we need to include all ids?
                token_ids.add(pydic_ids[0])

        res_array = []

        for valid_token_id in token_ids:
            res_array.append(create_token_description(valid_token_id))

        return res_array

    def __get_tokens_for_word_form_from_dic(self, form, dic_name):
        if dic_name not in self._dictionaries_map:
            raise NotRegisteredDictionaryException(dic_name)

        dic_instance = self._dictionaries_map[dic_name]
        return self.__get_tokens_from_dic(form, dic_instance)


class DictionaryUtils:
    __dictionary_manager = DictionaryManager([])
    __dictionary_storage_paths = set([])

    @staticmethod
    def add_dictionary_storages_paths(storage_paths_list):
        DictionaryUtils.__dictionary_storage_paths |= set((map(lambda x: str(x),
            filter(lambda x: os.path.exists(x),
                storage_paths_list))))

    @staticmethod
    def initialize():
        DictionaryUtils.__dictionary_manager = DictionaryManager(DictionaryUtils.__dictionary_storage_paths)

    @staticmethod
    def get_manager():
        return DictionaryUtils.__dictionary_manager
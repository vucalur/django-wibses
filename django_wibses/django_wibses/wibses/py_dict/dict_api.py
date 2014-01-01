import os

from pydic import PyDic
from repoze.lru import lru_cache

from ..utils import get_folder_containing_names, merge_into_path
from .. import JSON_INDENT, PYDIC_WORDS_CACHE_SIZE
from . import PYDIC_TOKEN_DESC__DICTIONARY, PYDIC_TOKEN_DESC__ID, PYDIC_TOKEN_DESC__BASE, \
    PYDIC_TOKEN_DESC__FORMS, PYDIC_TOKEN_DESC__TYPE, PYDIC_TOKEN_DESC__TYPE_TOKEN, PYDIC_TOKEN_DESC__TYPE_QUOTATION
from ..utils import dump_json


class NotRegisteredDictionaryException(Exception):
    def __init__(self, dic_name):
        Exception.__init__(self, 'Dictionary ' + str(dic_name) + ' was not registered in manager')
        self._dic_name = dic_name

    def get_dic_name(self):
        return self._dic_name


class DictionaryManager:
    def __init__(self, dictionaries_storages_list):
        print 'Initializing dictionary manager...'

        self._dictionaries_map = dict()
        self._current_unique_ids = set()

        valid_dicts_count = 0

        for storage in dictionaries_storages_list:
            storage_list_dicts = get_folder_containing_names(storage, incl_dir_names=True)
            for dic_dir in storage_list_dicts:
                dic_dir = merge_into_path([storage, dic_dir])
                assert isinstance(dic_dir, str)
                dic_name = dic_dir.split(os.sep)[-1]

                status = '\t-load dictionary %s' % dic_dir
                try:
                    dic_instance = PyDic(dic_dir)
                    self._dictionaries_map[dic_name] = dic_instance
                    status += ' [OK]'
                    valid_dicts_count += 1
                except Exception as e:
                    status += ' [ERROR] : %s' % str(e)

                print status

        print 'Dictionary manager has been initialized with %d dictionaries.\n' % valid_dicts_count

    @lru_cache(maxsize=PYDIC_WORDS_CACHE_SIZE)
    def __token_for_word(self, token_pydic_id, dic_instance):

        token_id = str(token_pydic_id)
        base_form = dic_instance.id_base(token_id)
        forms = dic_instance.id_forms(token_id)

        return {
            PYDIC_TOKEN_DESC__DICTIONARY: dic_instance.name,
            PYDIC_TOKEN_DESC__ID: token_id,
            PYDIC_TOKEN_DESC__BASE: base_form,
            PYDIC_TOKEN_DESC__FORMS: forms,
            PYDIC_TOKEN_DESC__TYPE: PYDIC_TOKEN_DESC__TYPE_TOKEN
        }

    @lru_cache(maxsize=100)
    def get_tokens_for_word_form(self, form):
        self._current_unique_ids = set()

        result = [
            {
                PYDIC_TOKEN_DESC__BASE: form,
                PYDIC_TOKEN_DESC__ID: '-',
                PYDIC_TOKEN_DESC__TYPE: PYDIC_TOKEN_DESC__TYPE_QUOTATION,
                PYDIC_TOKEN_DESC__DICTIONARY: "-",
                PYDIC_TOKEN_DESC__FORMS: [form]
            }
        ]

        result_tail = []
        for registered_dic in self._dictionaries_map.values():
            result_tail.extend(self.__get_tokens_from_dic(form, registered_dic))

        result_tail.sort(key=lambda x: x[PYDIC_TOKEN_DESC__BASE])
        result.extend(result_tail)

        return dump_json(result, JSON_INDENT)

    def __get_tokens_from_dic(self, form, dic_instance):

        def get_unique_ids(words):
            ids = set()
            for word in words:
                pydic_ids = dic_instance.id(word)
                if len(pydic_ids) > 0:
                    ids.add(pydic_ids[0])
            return ids

        possible_words = dic_instance.words_for_prefix(form)
        res_array = []

        for pydic_id in get_unique_ids(possible_words):
            res_array.append(self.__token_for_word(pydic_id, dic_instance))

        return res_array

    def __get_tokens_for_word_form_from_dic(self, form, dic_name):
        if dic_name not in self._dictionaries_map:
            raise NotRegisteredDictionaryException(dic_name)

        dic_instance = self._dictionaries_map[dic_name]
        return self.__get_tokens_from_dic(form, dic_instance)


class DictionaryUtils:
    __dictionary_manager = None
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
    def get_dict_manager():
        if DictionaryUtils.__dictionary_manager is None:
            raise Exception('Dictionary manager is not initialized')

        return DictionaryUtils.__dictionary_manager
import os
from django.http import HttpResponse
from dict_api import DictionaryUtils
from ..utils import jsonp
from .. import ENV_DIC_STORAGE_PATH_NAME, DEFAULT_PYDIC_STORAGES

DictionaryUtils.add_dictionary_storages_paths(os.environ.get(ENV_DIC_STORAGE_PATH_NAME, DEFAULT_PYDIC_STORAGES))
DictionaryUtils.initialize()


@jsonp
def rest__get_tokens(request, token_form):
    result_json = DictionaryUtils.get_manager().get_tokens_for_word_form(token_form)
    return HttpResponse(result_json)

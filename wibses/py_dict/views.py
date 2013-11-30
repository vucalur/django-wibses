from django.http import HttpResponse
from wibses.py_dict.dict_api import DictionaryUtils


# DictionaryUtils.add_dictionary_storages_paths(getattr(settings, 'PYDIC_STORAGES'))
# DictionaryUtils.initialize_from_current_config()


def rest__get_tokens(request, token_form):
    result_json = DictionaryUtils.get_manager().get_tokens_for_word_form(token_form)
    return HttpResponse(result_json, mimetype='application/json')
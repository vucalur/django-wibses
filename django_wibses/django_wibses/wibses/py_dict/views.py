from django.http import HttpResponse
from dict_api import DictionaryUtils
from ..utils import jsonp


@jsonp
def rest__get_tokens(request, token_form):
    result_json = DictionaryUtils.get_dict_manager().get_tokens_for_word_form(token_form)
    return HttpResponse(result_json)

import os
import tempfile
from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from wibses.dict_api import DictionaryUtils


DictionaryUtils.add_dictionary_storages_paths(getattr(settings, 'PYDIC_STORAGES'))
DictionaryUtils.initialize_from_current_config()


def get_storage_dir():
    return getattr(settings, 'JSONS_DIRECTORY', tempfile.gettempdir())


def store(string):
    storage_dir = get_storage_dir()
    with open(os.path.join(storage_dir, 'script_{date}.json'.format(date=datetime.now())), 'w') as f:
        f.write(string)


def load():
    storage_dir = get_storage_dir()
    with open(os.path.join(storage_dir, 'scriptMock.json'), 'r') as f:
        return f.read()

# TODO vucalur: fully enable csrf protection - somehow it's not working on chromium - cookie settings ?
@csrf_exempt
def script(request):
    if request.method == 'GET':
        json_string = load()
        return HttpResponse(json_string, mimetype='application/json')
    elif request.method == 'POST':
    # TODO vucalur: make Django threat POST as ajax :
    #if not request.is_ajax():  raise Http404 else:
        json_string = request.body
        try:
            store(json_string)
            return HttpResponse('Ok - saved')
        except KeyError:
            HttpResponseServerError('Malformed data!')


def token(request, token_form):
    result_json = DictionaryUtils.get_manager().get_tokens_for_word_form(token_form)
    return HttpResponse(result_json, mimetype='application/json')
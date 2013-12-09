import json
import os

from . import ASCI_GENERATOR_ALPHABET
from data_store import JSON_INDENT
from data_store.exceptions import NotJsonObjectException


def get_folder_containing_names(path, incl_file_names=False, incl_dir_names=False):
    if not (incl_dir_names or incl_file_names):
        return None

    from os import walk

    for dir_name, dir_names, file_names in walk(path):
        if incl_file_names and incl_dir_names:
            return dir_names, file_names
        elif incl_dir_names:
            return dir_names
        elif incl_file_names:
            return file_names


def merge_into_path(files_paths_list):
    result_path = files_paths_list[0]
    if len(files_paths_list) > 1:
        for path in files_paths_list[1:]:
            result_path += os.sep + path

    while True:
        old_len = len(result_path)
        result_path = result_path.replace(os.sep*2, os.sep)
        if old_len == len(result_path):
            break

    return result_path


def get_repo_dir_name_for_script_filename(script_name):
    return "." + script_name


def get_script_file_name_from_repo_dir_name(repo_dir_name):
    return repo_dir_name[1:]


def jsonp(f):
    """
    Wrap a json response in a callback, and set the mimetype (Content-Type) header accordingly
    (will wrap in text/javascript if there is a callback). If the "callback" or "jsonp" paramters
    are provided, will wrap the json output in callback({thejson})

    Usage:

    @jsonp
    def my_json_view(request):
        d = { 'key': 'value' }
        return HTTPResponse(json.dumps(d), content_type='application/json')


    Based on: https://gist.github.com/sivy/871954
    """
    from functools import wraps

    @wraps(f)
    def jsonp_wrapper(request, *args, **kwargs):
        resp = f(request, *args, **kwargs)
        if resp.status_code != 200:
            return resp

        callback = None
        if 'callback' in request.GET:
            callback = request.GET['callback']
        elif 'jsonp' in request.GET:
            callback = request.GET['jsonp']
        else:
            return resp

        resp['Content-Type'] = 'application/javascript; charset=utf-8'
        resp.content = "%s(%s);" % (callback, resp.content)
        return resp

    return jsonp_wrapper


class ASCIIdGenerator:
    def __init__(self, positions_count):
        self._positions_count = positions_count
        self._my_alphabet = list(set(ASCI_GENERATOR_ALPHABET))
        self._current_indexes = [0] * positions_count
        self._alph_length = len(self._my_alphabet)

    def __fall_over(self):
        idx = self._positions_count - 1
        self._current_indexes[idx] += 1
        move = 0

        while idx >= 0:
            curr_idx = self._current_indexes[idx]
            new_val = curr_idx + move
            self._current_indexes[idx] = new_val % self._alph_length
            move = new_val / self._alph_length
            idx -= 1

    def next_id(self):
        result = ""
        for idx in self._current_indexes:
            result += self._my_alphabet[idx]

        self.__fall_over()

        return result


def read_script_object(file_path):
    f = open(file_path, "r")
    json_txt = f.read().replace("\n", "")
    f.close()

    try:
        return json.loads(json_txt)
    except Exception:
        raise NotJsonObjectException(json_txt)


def write_script_object(file_path, script_object):
    f = open(file_path, "w")
    try:
        json_txt = json.dumps(script_object, indent=JSON_INDENT)
    except Exception:
        f.close()
        raise NotJsonObjectException(str(script_object))

    f.write(json_txt)
    f.close()
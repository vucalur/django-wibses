import os
import json

from django.conf import settings

from pydic import PyDic
from wibses import polish_alphabet


_current_pydic_singleton = None


def get_current_pydic():
    global _current_pydic_singleton
    if _current_pydic_singleton is None:
        pydic_full_project_path = getattr(settings, 'PYDIC_DIR', '.') + \
                                  os.sep + getattr(settings, 'CURRENT_PYDIC_NAME ', 'sjp.pydic')
        print pydic_full_project_path
        _current_pydic_singleton = PyDic(pydic_full_project_path)
    return _current_pydic_singleton


def prepare_possible_polish_words(token_form, max_suffix_length=3):
    alphabet = polish_alphabet

    def appender(suffix, max_suffix_length, curr_lev=1):
        if curr_lev <= max_suffix_length:
            result = [token_form + suffix]
            for letter in alphabet:
                result.extend(appender(suffix + letter, max_suffix_length, curr_lev + 1))
            return result
        return []

    return appender('', max_suffix_length)


def prepare_json_result_array_part(pydic_id):
    token_id = str(pydic_id)
    base_form = get_current_pydic().id_base(token_id)
    forms = get_current_pydic().id_forms(token_id)
    return {'token_id': token_id, 'token_base': base_form, 'token_forms': forms}


def prepare_token_json(token_form):
    possible_words = prepare_possible_polish_words(token_form)
    token_ids = set([])
    for word in possible_words:
        pydic_ids = get_current_pydic().id(word)
        if len(pydic_ids) > 0:
            token_ids.add(pydic_ids[0])
    if len(token_ids) == 0:
        return json.dumps({'exists': False, 'forms': []}, indent=3)
    else:
        res_array = []
        for valid_token_id in token_ids:
            res_array.append(prepare_json_result_array_part(valid_token_id))
        return json.dumps({'exists': True, 'forms': res_array}, indent=3)
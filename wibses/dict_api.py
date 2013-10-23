import os
import json

from django.conf import settings

from pydic import PyDic


_current_pydic_singleton = None


def get_current_pydic():
    global _current_pydic_singleton
    if _current_pydic_singleton is None:
        pydic_full_project_path = getattr(settings, 'PYDIC_DIR', '.') + \
                                  os.sep + getattr(settings, 'CURRENT_PYDIC_NAME ', 'sjp.pydic')
        print pydic_full_project_path
        _current_pydic_singleton = PyDic(pydic_full_project_path)
    return _current_pydic_singleton


def prepare_json_result_array_part(pydic_id):
    token_id = str(pydic_id)
    base_form = get_current_pydic().id_base(token_id)
    forms = get_current_pydic().id_forms(token_id)
    return {'dic': get_current_pydic().name, 'id': token_id, 'base': base_form, 'forms': forms, 'type': "token"}


def prepare_token_json(token_form):
    possible_words = get_current_pydic().forms_for_prefix(token_form)
    token_ids = set([])
    for word in possible_words:
        pydic_ids = get_current_pydic().id(word)
        if len(pydic_ids) > 0:
            token_ids.add(pydic_ids[0])

    res_array = [{'base': token_form, 'type': 'quotation', 'dic': "-", 'forms': [token_form]}]
    for valid_token_id in token_ids:
        res_array.append(prepare_json_result_array_part(valid_token_id))
    return json.dumps(res_array, indent=3)
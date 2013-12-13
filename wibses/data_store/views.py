import os
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from . import REQUEST_PARAM_NAME__USER, HTTP__OK_RESPONSE, \
    REQUEST_PARAM_NAME_ACTION, REQUEST_PARAM_NAME__SCRIPT_ID, REQUEST_PARAM_NAME__SCRIPT_REVISION, \
    REQUEST_PARAM_NAME__STORAGE_FILENAME
from exceptions import MissingRequestParamException, NotProperRequestTypeForUrl, \
    RequestTypeDoesNotSupportedException, NotSupportedApiActionException
from script_api import ScriptUtils
from validation import get_semantic_validator
from .. import JSON_TEMPLATE_SCRIPT_FILENAME, ENV_SCRIPT_STORAGE_PATH_NAME, DEFAULT_SCRIPT_STORAGE


ScriptUtils.set_script_template_filename(JSON_TEMPLATE_SCRIPT_FILENAME)
ScriptUtils.set_scripts_storage_path(os.environ.get(ENV_SCRIPT_STORAGE_PATH_NAME, DEFAULT_SCRIPT_STORAGE))
ScriptUtils.initialize()

#region REST url functions mapping

#region REST help functions


def create_http_json_response(json_response):
    return HttpResponse(json_response, content_type='application/json')


def http_ok_response():
    return HttpResponse(HTTP__OK_RESPONSE)


def process_request_params(request_dict, param_names):
    params_values_dict = dict()
    lost_params = []
    for p in param_names:
        p_value = request_dict.get(p, None)
        if p_value is None:
            lost_params.append(p)
        else:
            params_values_dict[p] = p_value
    if len(lost_params) > 0:
        raise MissingRequestParamException(lost_params)
    return params_values_dict


# noinspection PyUnusedLocal
def get_only(function, *args, **kwargs):
    def decorator(*args, **kwargs):
        if args[0].method != 'GET':
            raise NotProperRequestTypeForUrl('GET', args[0].method)
        return function(*args, **kwargs)

    return decorator


# noinspection PyUnusedLocal
def post_only(function, *args, **kwargs):
    def decorator(*args, **kwargs):
        if args[0].method != 'POST':
            raise NotProperRequestTypeForUrl('POST', args[0].method)
        return function(*args, **kwargs)

    return decorator


# noinspection PyUnusedLocal
def handle_exceptions(function, *args, **kwargs):
    def decorator(*args, **kwargs):
        try:
            k = function(*args, **kwargs)
            return k
        except Exception as e:
            return HttpResponseServerError(str(e))

    return decorator


def validate_request_json(function, *args, **kwargs):
    def decorator(*args, **kwargs):
        get_semantic_validator().validate_script(args[0].body)
        return function(*args, **kwargs)

    return decorator

#endregion


#OK
@handle_exceptions
@get_only
def rest__get_script(request, script_id=None, get_from_params=False):
    if get_from_params:
        params = process_request_params(request.GET, [REQUEST_PARAM_NAME__SCRIPT_ID])
        script_id = params[REQUEST_PARAM_NAME__SCRIPT_ID]
    script_json = ScriptUtils.get_manager().get_script(script_id)
    return create_http_json_response(script_json)


#OK
@handle_exceptions
@get_only
def rest__list_storage_scripts(request, get_from_params=False):
    scripts_json_array = ScriptUtils.get_manager().get_scripts_in_storage_json()
    return create_http_json_response(scripts_json_array)


#OK
@csrf_exempt
@handle_exceptions
@post_only
@validate_request_json
def rest__save_script_in_storage(request, script_id=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER,
                                                              REQUEST_PARAM_NAME__SCRIPT_ID])
        script_id = request_params[REQUEST_PARAM_NAME__SCRIPT_ID]
    else:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER])

    curr_user = request_params[REQUEST_PARAM_NAME__USER]
    script_body = request.body
    ScriptUtils.get_manager().update_script_in_storage(script_id, script_body, curr_user)
    return http_ok_response()


#OK
@handle_exceptions
@get_only
def rest__list_script_history(request, script_id=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__SCRIPT_ID])
        script_id = request_params[REQUEST_PARAM_NAME__SCRIPT_ID]

    scripts_history_json_array = ScriptUtils.get_manager().get_script_history_json(script_id)
    return create_http_json_response(scripts_history_json_array)


#OK
@handle_exceptions
@get_only
def rest__get_script_of_revision(request, script_id=None, revision=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__SCRIPT_ID,
                                                              REQUEST_PARAM_NAME__SCRIPT_REVISION])
        script_id = request_params[REQUEST_PARAM_NAME__SCRIPT_ID]
        revision = request_params[REQUEST_PARAM_NAME__SCRIPT_REVISION]

    scripts_json = ScriptUtils.get_manager().get_script_revision(script_id, revision)
    return create_http_json_response(scripts_json)


@handle_exceptions
@get_only
def rest__fork_script_of_revision(request, script_id=None, revision=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET,
            [REQUEST_PARAM_NAME__USER,
             REQUEST_PARAM_NAME__SCRIPT_ID,
             REQUEST_PARAM_NAME__SCRIPT_REVISION,
             REQUEST_PARAM_NAME__STORAGE_FILENAME])
        script_id = request_params[REQUEST_PARAM_NAME__SCRIPT_ID]
        revision = request_params[REQUEST_PARAM_NAME__SCRIPT_REVISION]
    else:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER,
                                                              REQUEST_PARAM_NAME__STORAGE_FILENAME])
    user_name = request_params[REQUEST_PARAM_NAME__USER]
    storage_filename = request_params[REQUEST_PARAM_NAME__STORAGE_FILENAME]

    scripts_json = ScriptUtils.get_manager().fork_script_of_revision(script_id, revision, user_name, storage_filename)
    return create_http_json_response(scripts_json)


#OK
@handle_exceptions
@get_only
def rest__create_new_script(request, get_from_params=False):
    request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER,
                                                          REQUEST_PARAM_NAME__STORAGE_FILENAME])

    curr_user = request_params[REQUEST_PARAM_NAME__USER]
    storage_filename = request_params[REQUEST_PARAM_NAME__STORAGE_FILENAME]
    new_script_json = ScriptUtils.get_manager().create_script_in_repo(curr_user, storage_filename)
    return create_http_json_response(new_script_json)


__api_dictionary = {
    'script': rest__get_script,
    'list': rest__list_storage_scripts,
    'store': rest__save_script_in_storage,
    'create': rest__create_new_script,
    'fork': rest__fork_script_of_revision,
    'getrev': rest__get_script_of_revision,
    'hist': rest__list_script_history
}


@csrf_exempt
@handle_exceptions
def rest__params_api(request):
    if not (request.method == 'POST' or request.method == 'GET'):
        raise RequestTypeDoesNotSupportedException(request.method, ['POST', 'GET'])

    params = process_request_params(request.GET, [REQUEST_PARAM_NAME_ACTION])
    global __api_dictionary

    action = params[REQUEST_PARAM_NAME_ACTION]
    action_handler = __api_dictionary.get(action, None)
    if action_handler is None:
        raise NotSupportedApiActionException(action, list(__api_dictionary.keys()))

    return action_handler(request, get_from_params=True)

#endregion
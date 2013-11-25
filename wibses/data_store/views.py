
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from wibses.data_store import REQUEST_PARAM_NAME__USER, HTTP__OK_RESPONSE, REQUEST_PARAM_NAME__NEW_SCRIPT_NAME, REQUEST_PARAM_NAME_ACTION, REQUEST_PARAM_NAME__SCRIPT_NAME, REQUEST_PARAM_NAME__SCRIPT_REVISION
from wibses.data_store.exceptions import MissingRequestParamException, NotProperRequestTypeForUrl, RequestTypeDoesNotSupportedException, NotSupportedApiActionException

from wibses.data_store.script_api import ScriptUtils


ScriptUtils.set_dictionary_storage_path(getattr(settings, 'SCRIPT_STORAGE'))
ScriptUtils.set_script_template_filename(getattr(settings, 'JSON_TEMPLATE_SCRIPT_FILENAME'))
ScriptUtils.initialize_from_current_config()


#region REST url functions mapping

#region REST help functions

def create_http_json_response(json_response):
    return HttpResponse(json_response, mimetype='application/json')


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

#endregion


#OK
@handle_exceptions
@get_only
def rest__get_script(request, script_name=None, get_from_params=False):
    if get_from_params:
        params = process_request_params(request.GET, [REQUEST_PARAM_NAME__SCRIPT_NAME])
        script_name = params[REQUEST_PARAM_NAME__SCRIPT_NAME]
    script_json = ScriptUtils.get_manager().get_script(script_name)
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
def rest__save_script_in_storage(request, script_name=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER,
                                                               REQUEST_PARAM_NAME__SCRIPT_NAME])
        script_name = request_params[REQUEST_PARAM_NAME__SCRIPT_NAME]
    else:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER])

    curr_user = request_params[REQUEST_PARAM_NAME__USER]
    script_body = request.body
    ScriptUtils.get_manager().update_script_in_storage(script_name, script_body, curr_user)
    return http_ok_response()


#OK
@handle_exceptions
@get_only
def rest__list_script_history(request, script_name=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__SCRIPT_NAME])
        script_name = request_params[REQUEST_PARAM_NAME__SCRIPT_NAME]

    scripts_history_json_array = ScriptUtils.get_manager().get_script_history_json(script_name)
    return create_http_json_response(scripts_history_json_array)


#OK
@handle_exceptions
@get_only
def rest__get_script_of_revision(request, script_name=None, revision=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__SCRIPT_NAME,
                                                              REQUEST_PARAM_NAME__SCRIPT_REVISION])
        script_name = request_params[REQUEST_PARAM_NAME__SCRIPT_NAME]
        revision = request_params[REQUEST_PARAM_NAME__SCRIPT_REVISION]

    scripts_json = ScriptUtils.get_manager().get_script_revision(script_name, revision)
    return create_http_json_response(scripts_json)


@handle_exceptions
@get_only
def rest__fork_script_of_revision(request, script_name=None, revision=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET,
                                                [REQUEST_PARAM_NAME__USER,
                                                REQUEST_PARAM_NAME__NEW_SCRIPT_NAME,
                                                REQUEST_PARAM_NAME__SCRIPT_NAME])
        script_name = request_params[REQUEST_PARAM_NAME__SCRIPT_NAME]
    else:
        request_params = process_request_params(request.GET,
                                                [REQUEST_PARAM_NAME__USER,
                                                 REQUEST_PARAM_NAME__NEW_SCRIPT_NAME])
    new_script_name = request_params[REQUEST_PARAM_NAME__NEW_SCRIPT_NAME]
    user_name = request_params[REQUEST_PARAM_NAME__USER]

    scripts_json = ScriptUtils.get_manager().fork_script_of_revision(script_name, revision, new_script_name, user_name)
    return create_http_json_response(scripts_json)


#OK
@handle_exceptions
@get_only
def rest__create_new_script(request, script_name=None, get_from_params=False):
    if get_from_params:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER,
                                                              REQUEST_PARAM_NAME__SCRIPT_NAME])
        script_name = request_params[REQUEST_PARAM_NAME__SCRIPT_NAME]
    else:
        request_params = process_request_params(request.GET, [REQUEST_PARAM_NAME__USER])

    curr_user = request_params[REQUEST_PARAM_NAME__USER]
    new_script_json = ScriptUtils.get_manager().create_script_in_repo(script_name, curr_user)
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
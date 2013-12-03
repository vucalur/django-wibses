from wibses.data_store import HTTP__EXCEPTION_TAG__MISSING_PARAMS, HTTP__EXCEPTION_TAG__NOT_PROPER_REQUEST_TYPE, \
    HTTP__EXCEPTION_TAG__NO_SUCH_SCRIPT_IN_STORAGE, HTTP__EXCEPTION_TAG__BAD_SCRIPT_REVISION,\
    HTTP__EXCEPTION_TAG__SCRIPT_ALREADY_IN_STORAGE, HTTP__EXCEPTION_TAG__NOT_SUPPORTED_REQUEST_TYPE, \
    HTTP__EXCEPTION_TAG__NOT_SUPPORTED_ACTION, HTTP__EXCEPTION_TAG__NOT_VALID_JSON_SCRIPT, HTTP__EXCEPTION_TAG__NOT_JSON_OBJECT


class MissingRequestParamException(Exception):
    def __init__(self, param_list):
        self._missing_params = param_list
        description = HTTP__EXCEPTION_TAG__MISSING_PARAMS + " : "
        for p in param_list:
            description += '"%s"; ' % str(p)
        Exception.__init__(self, description)

    def get_missing_params(self):
        return self._missing_params


class NotProperRequestTypeForUrl(Exception):
    def __init__(self, perm_type, actual_type):
        description = HTTP__EXCEPTION_TAG__NOT_PROPER_REQUEST_TYPE + \
            " : Permitted request type -> %s ; Actual -> %s" % (str(perm_type), str(actual_type))
        self._permitted = perm_type
        self._actual = actual_type
        Exception.__init__(self, description)

    def get_permitted_type(self):
        return self._permitted

    def get_actual_type(self):
        return self._actual


class NoSuchScriptInStorageException(Exception):
    def __init__(self, script_name):
        description = HTTP__EXCEPTION_TAG__NO_SUCH_SCRIPT_IN_STORAGE + \
            ": %s" % script_name
        self._script_name = script_name
        Exception.__init__(self, description)

    def get_script_name(self):
        return self._script_name


class BadScriptRevisionException(Exception):
    def __init__(self, revision):
        description = HTTP__EXCEPTION_TAG__BAD_SCRIPT_REVISION + \
            ": %s" % revision
        self._revision = revision
        Exception.__init__(self, description)

    def get_revision(self):
        return self._revision


class ScriptAlreadyExistsInStorageException(Exception):
    def __init__(self, script_name):
        description = HTTP__EXCEPTION_TAG__SCRIPT_ALREADY_IN_STORAGE + \
            ": %s" % script_name
        self._script_name = script_name
        Exception.__init__(self, description)

    def get_script_name(self):
        return self._script_name


class RequestTypeDoesNotSupportedException(Exception):
    def __init__(self, request_type, supported_request_types):
        description = HTTP__EXCEPTION_TAG__NOT_SUPPORTED_REQUEST_TYPE + \
            ": '%s' . Supported are: " % request_type
        for rt in supported_request_types:
            description += rt + "; "
        self._request_type = request_type
        self._supported_requests = supported_request_types
        Exception.__init__(self, description)

    def get_request_type(self):
        return self._request_type

    def get_supported_request_types(self):
        return self._supported_requests


class NotSupportedApiActionException(Exception):
    def __init__(self, action, supported_actions):
        self._supported_actions = supported_actions
        self._action = action
        description = HTTP__EXCEPTION_TAG__NOT_SUPPORTED_ACTION + \
            ": '%s' . Supported are: " % action
        for sa in supported_actions:
            description += sa + "; "
        Exception.__init__(self, description)

    def get_action(self):
        return self._action

    def get_supported_actions(self):
        return self._supported_actions


class ScriptValidationException(Exception):
    def __init__(self, errors_list):
        self._errors = errors_list
        description = HTTP__EXCEPTION_TAG__NOT_VALID_JSON_SCRIPT + ": "
        for error in errors_list:
            description += error.get_err_msg() + " in " + error.get_place() + ";  "
        Exception.__init__(self, description)

    def get_errors(self):
        return self._errors


class NotJsonObjectException(Exception):
    def __init__(self, not_json_object):
        self._passed_object = not_json_object
        description = '%s: passed object : %s' % (HTTP__EXCEPTION_TAG__NOT_JSON_OBJECT, str(not_json_object))
        Exception.__init__(self, description)

    def get_passed_object(self):
        return self._passed_object
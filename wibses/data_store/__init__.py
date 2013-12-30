#responses tags
HTTP__EXCEPTION_TAG__MISSING_PARAMS = '_MissingRequestParams_'
HTTP__EXCEPTION_TAG__NOT_PROPER_REQUEST_TYPE = '_BadRequestTypeForUrl_'
HTTP__EXCEPTION_TAG__NO_SUCH_SCRIPT_IN_STORAGE = '_ScriptIdDoesNotExist_'
HTTP__EXCEPTION_TAG__BAD_SCRIPT_REVISION = '_BadScriptRevision_'
HTTP__EXCEPTION_TAG__SCRIPT_ALREADY_IN_STORAGE = '_ScriptAlreadyInStorage_'
HTTP__EXCEPTION_TAG__NOT_SUPPORTED_REQUEST_TYPE = '_RequestTypeDoesNotSupported_'
HTTP__EXCEPTION_TAG__NOT_SUPPORTED_ACTION = '_NotSupportedAction_'
HTTP__EXCEPTION_TAG__NOT_VALID_JSON_SCRIPT = '_JsonScriptNotValid_'
HTTP__EXCEPTION_TAG__NOT_JSON_OBJECT = '_NotAJsonObject_'

HTTP__OK_RESPONSE = '_OK_'

#request params names
REQUEST_PARAM_NAME__USER = 'user'
REQUEST_PARAM_NAME__NEW_SCRIPT_NAME = 'new_name'
REQUEST_PARAM_NAME_ACTION = 'action'
REQUEST_PARAM_NAME__SCRIPT_ID = 'script_id'
REQUEST_PARAM_NAME__SCRIPT_REVISION = 'revision'
REQUEST_PARAM_NAME__STORAGE_FILENAME = "storage_filename"


#json keywords
JSON_ATTR_NAME__REVISION = 'revision'
JSON_ATTR_NAME__MODIFIED_DATE = 'modified_date'
JSON_ATTR_NAME__CHANGER = 'changer_user'
JSON_ATTR_NAME__PARAMS = "params"
JSON_ATTR_NAME__NAME = "name"
JSON_ATTR_NAME__ID = "id"
JSON_ATTR_SCRIPT_ID = "script_id"


#storage default conf
STORAGE_DEFAULT_SCAN_PERIOD_MS = 1000
DEFAULT_STORAGE_SCRIPT_CREATOR_NAME = 'autostore'
STORAGE_ID_GENERATOR_POSITIONS_COUNT = 10


#repo configuration
REPO_CONF_FILENAME = 'repo.conf'
REPO_CONF_SECTION__SCRIPT_INFO = 'script_info'
REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP = 'original_filename'

REPO_GITIGNORE_FILENAME = '.gitignore'
REPO_IGNORED_FILENAMES = [REPO_GITIGNORE_FILENAME, REPO_CONF_FILENAME]

#other configs
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

#script format configuration constants
SCR_FORMAT_CONF__MAIN = 'main'
SCR_FORMAT_CONF__TYPE = 'type'
SCR_FORMAT_CONF__S_TYPE_BOOL = 'bool'
SCR_FORMAT_CONF__S_TYPE_INT = 'int'
SCR_FORMAT_CONF__S_TYPE_STR = 'str'
SCR_FORMAT_CONF__S_TYPE_NUM = 'num'
SCR_FORMAT_CONF__C_TYPE_OBJ = 'obj'
SCR_FORMAT_CONF__C_TYPE_ARRAY = 'arr'
SCR_FORMAT_CONF__ENUM = 'enum'
SCR_FORMAT_CONF__ALL_PROPS = 'all'
SCR_FORMAT_CONF__NAME = 'name'
SCR_FORMAT_CONF__ITEMS = 'items'
SCR_FORMAT_CONF__REQUIRED = 'r'
SCR_FORMAT_CONF__NOT_REQUIRED = 'nr'
SCR_FORMAT_CONF__MIN = 'min'
SCR_FORMAT_CONF__MAX = 'max'
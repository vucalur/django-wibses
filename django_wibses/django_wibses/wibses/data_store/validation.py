from ConfigParser import NoOptionError, NoSectionError
import ConfigParser
import json
import os
import traceback
import jsonschema as js_schema_validate

from . import SCR_FORMAT_CONF__ALL_PROPS, SCR_FORMAT_CONF__S_TYPE_INT, SCR_FORMAT_CONF__S_TYPE_STR, \
    SCR_FORMAT_CONF__S_TYPE_NUM, SCR_FORMAT_CONF__C_TYPE_OBJ, SCR_FORMAT_CONF__ENUM, SCR_FORMAT_CONF__S_TYPE_BOOL, \
    SCR_FORMAT_CONF__TYPE, SCR_FORMAT_CONF__C_TYPE_ARRAY, SCR_FORMAT_CONF__NAME, SCR_FORMAT_CONF__MIN, \
    SCR_FORMAT_CONF__MAX, SCR_FORMAT_CONF__ITEMS, SCR_FORMAT_CONF__MAIN, SCR_FORMAT_CONF__REQUIRED, \
    SCR_FORMAT_CONF__NOT_REQUIRED, SCR_FORMAT_CONF__DEFAULT, JSON_SCHEMA_DEFAULT_VAL
import sys
from exceptions import ScriptValidationException, NotJsonObjectException, ScriptFormatConfigurationException
from .. import SCRIPT_FORMAT_CONFIG_FILE


_simple_type_translation_dict = {
    SCR_FORMAT_CONF__S_TYPE_INT: 'integer',
    SCR_FORMAT_CONF__S_TYPE_STR: 'string',
    SCR_FORMAT_CONF__S_TYPE_NUM: 'number',
    SCR_FORMAT_CONF__ENUM: 'enum',
    SCR_FORMAT_CONF__S_TYPE_BOOL: 'boolean'
}

_simple_type_default_value_translation = {
    SCR_FORMAT_CONF__S_TYPE_INT: lambda x: int(x),
    SCR_FORMAT_CONF__S_TYPE_STR: lambda x: x,
    SCR_FORMAT_CONF__S_TYPE_NUM: lambda x: float(x),
    SCR_FORMAT_CONF__S_TYPE_BOOL: lambda x: str(x).lower() in ('true', 't', '1')
}

_complex_type_translation_dict = {
    SCR_FORMAT_CONF__C_TYPE_ARRAY: "array",
    SCR_FORMAT_CONF__C_TYPE_OBJ: 'object',
    SCR_FORMAT_CONF__S_TYPE_STR: 'string',
}


class ScriptValidationError:
    def __init__(self, js_validation_error):
        self._error_message = js_validation_error.message
        err_path = 'script'
        for p in js_validation_error.path:
            if isinstance(p, int):
                err_path += '[%d]' % (p + 1)
            else:
                err_path += '/%s' % p
        self._error_place = err_path

    def get_err_msg(self):
        return self._error_message

    def get_place(self):
        return self._error_place


def secure_option_value_get(config, section_name, option_name):
    try:
        return config.get(section_name, option_name)
    except Exception:
        return None


def __encode_obj_prop(configuration, section_name):

    global _simple_type_translation_dict, _simple_type_default_value_translation

    #returns (name, conv_type, default_value, is_required)
    def check_simple_prop(prop_conf):
        name = prop_conf[0]
        if prop_conf[3] == SCR_FORMAT_CONF__REQUIRED:
            required = True
        elif prop_conf[3] == SCR_FORMAT_CONF__NOT_REQUIRED:
            required = False
        else:
            raise ScriptFormatConfigurationException("""Error property value '%s'.
            Syntax : <name[:simple_type_name:default_value]:(%s|%s)>""" % (prop_conf,
                                                                           SCR_FORMAT_CONF__REQUIRED,
                                                                           SCR_FORMAT_CONF__NOT_REQUIRED))

        prop_type = _simple_type_translation_dict.get(prop_conf[1], None)
        prop_default_translator = _simple_type_default_value_translation.get(prop_conf[1], None)
        if prop_type is None or prop_default_translator is None:
            raise ScriptFormatConfigurationException("Not supported type of property %s. Support one of %s"
                                                     % (prop_conf[1], str(list(_simple_type_translation_dict.keys()))))

        return name, prop_type, prop_default_translator(prop_conf[2]), required

    #returns (name, object, is_required)
    def check_complex_prop(prop_conf):
        name = prop_conf[0]

        if prop_conf[1] == SCR_FORMAT_CONF__REQUIRED:
            required = True
        elif prop_conf[1] == SCR_FORMAT_CONF__NOT_REQUIRED:
            required = False
        else:
            raise ScriptFormatConfigurationException("""Error property value '%s'.
                Syntax : <name:(%s|%s)>""" % (prop_conf, SCR_FORMAT_CONF__REQUIRED, SCR_FORMAT_CONF__NOT_REQUIRED))

        obj_descr = get_object_from_config(configuration, name)

        return obj_descr[0], obj_descr[1], required

    current_name = configuration.get(section_name, SCR_FORMAT_CONF__NAME)
    all_props = configuration.get(section_name, SCR_FORMAT_CONF__ALL_PROPS).split('|')

    simple_props = []
    complex_props = []

    for prop in all_props:
        prop_conf = prop.split(":")
        if len(prop_conf) == 2:
            complex_props.append(check_complex_prop(prop_conf))
        elif len(prop_conf) == 4:
            simple_props.append(check_simple_prop(prop_conf))
        else:
            raise ScriptFormatConfigurationException("""Error property value '%s'.
                Syntax : <name[:simple_type_name]:require_flag>""" % prop)

    required_arr_names = []
    properties_dict = {}

    for sp in simple_props:
        if sp[3]:
            required_arr_names.append(sp[0])
        properties_dict[sp[0]] = {
            "type": sp[1],
            JSON_SCHEMA_DEFAULT_VAL: sp[2]
        }
    for cp in complex_props:
        if cp[2]:
            required_arr_names.append(cp[0])
        properties_dict[cp[0]] = cp[1]

    return current_name, {
        "type": 'object',
        "properties": properties_dict,
        "additionalProperties": False,
        "required": required_arr_names
    }


def __encode_arr_prop(configuration, section_name):
    current_name = configuration.get(section_name, SCR_FORMAT_CONF__NAME)
    min_items = secure_option_value_get(configuration, section_name, SCR_FORMAT_CONF__MIN)
    max_items = secure_option_value_get(configuration, section_name, SCR_FORMAT_CONF__MAX)

    items_obj_section = configuration.get(section_name, SCR_FORMAT_CONF__ITEMS)
    items_obj_name, items_obj = get_object_from_config(configuration, items_obj_section)

    result_obj = {
        "type": "array",
        "items": items_obj
    }

    if min_items is not None:
        result_obj["minItems"] = int(min_items)
    if max_items is not None:
        result_obj["maxItems"] = int(max_items)

    return current_name, result_obj


def __encode_complex_str_prop(configuration, section_name):
    current_name = configuration.get(section_name, SCR_FORMAT_CONF__NAME)

    result_obj = {
        "type": "string"
    }

    enum_vals_str = secure_option_value_get(configuration, section_name, SCR_FORMAT_CONF__ENUM)
    if enum_vals_str is not None:
        result_obj["enum"] = enum_vals_str.split('|')

    min_length = secure_option_value_get(configuration, section_name, SCR_FORMAT_CONF__MIN)
    max_length = secure_option_value_get(configuration, section_name, SCR_FORMAT_CONF__MAX)
    default = configuration.get(section_name, SCR_FORMAT_CONF__DEFAULT)

    if min_length is not None:
        result_obj["minLength"] = int(min_length)
    if max_length is not None:
        result_obj["maxLength"] = int(max_length)

    result_obj[JSON_SCHEMA_DEFAULT_VAL] = default

    return current_name, result_obj


_encoder = {
    SCR_FORMAT_CONF__C_TYPE_ARRAY: __encode_arr_prop,
    SCR_FORMAT_CONF__C_TYPE_OBJ: __encode_obj_prop,
    SCR_FORMAT_CONF__S_TYPE_STR: __encode_complex_str_prop
}


def get_object_from_config(configuration, section_name):
    #returns (name, object)
    global _encoder

    try:
        current_type = configuration.get(section_name, SCR_FORMAT_CONF__TYPE)
        current_encoder = _encoder.get(current_type, None)
        if current_encoder is None:
            raise ScriptFormatConfigurationException("Not supported type of complex property '%s'. Supported one of %s"
                                                     % (current_type, list(_encoder.keys())))

        return current_encoder(configuration, section_name)
    except NoOptionError as e:
        raise ScriptFormatConfigurationException("Section '%s' must contain property '%s'" % (e.section, e.option))
    except NoSectionError as e:
        raise ScriptFormatConfigurationException("There is not section '%s' which was specified in other section"
                                                 % e.section)


def generate_obj_for_schema(schema_obj):
    required_props = schema_obj["required"]
    result_obj = {}

    for required_property_name in required_props:
        obj_description = schema_obj["properties"][required_property_name]
        generated_obj = generate_template_for_schema(obj_description)

        result_obj[required_property_name] = generated_obj

    return result_obj


def generate_arr_for_schema(schema_obj):
    min_length = schema_obj.get("minItems", 0)

    item_description = schema_obj["items"]
    generated_obj = generate_template_for_schema(item_description)

    return [generated_obj] * min_length


def generate_simple_type_val_for_schema(schema_obj):
    return schema_obj[JSON_SCHEMA_DEFAULT_VAL]

_generator_encoder = {
    "object": generate_obj_for_schema,
    "array": generate_arr_for_schema,
    "string": generate_simple_type_val_for_schema,
    "boolean": generate_simple_type_val_for_schema,
    "integer": generate_simple_type_val_for_schema,
    "number": generate_simple_type_val_for_schema
}


#returns object or array
def generate_template_for_schema(schema_obj):
    try:
        current_type = schema_obj["type"]
        return _generator_encoder[current_type](schema_obj)
    except Exception:
        print 'Error while creating template for new script'
        traceback.print_exc(sys.stderr)
        os.kill(os.getpid(), 1)


class ScriptFormatManager:
    def __init__(self):
        print 'Initializing script format manager...'

        self._schema = None
        self._validator = None
        self._script_template = None

        self.__load_schema()

        print 'Script format manager has been initialized\n'

    def __load_schema(self):
        configuration = ConfigParser.ConfigParser()
        try:
            configuration.readfp(open(SCRIPT_FORMAT_CONFIG_FILE, 'r'))
            dummy, schema = get_object_from_config(configuration, SCR_FORMAT_CONF__MAIN)
            self._schema = schema
        except Exception:
            print 'Error while loading script format configuration'
            traceback.print_exc(sys.stderr)
            os.kill(os.getpid(), 1)

        self._validator = js_schema_validate.Draft4Validator(self._schema)
        self._script_template = generate_template_for_schema(self._schema)

    def get_schema(self):
        return self._schema

    def get_script_template(self):
        return self._script_template

    def validate_script(self, json_obj, is_text=True, with_raise=True):
        if is_text:
            try:
                json_obj = json.loads(json_obj)
            except Exception:
                raise NotJsonObjectException(json_obj)

        errors = sorted(self._validator.iter_errors(json_obj), key=lambda e: e.path)
        if len(errors) == 0:
            return True

        if not with_raise:
            return False

        errors_wrappers = []
        for err in errors:
            errors_wrappers.append(ScriptValidationError(err))

        raise ScriptValidationException(errors_wrappers)

    def validate_script_file(self, file_path):
        f = open(file_path, "r")
        script_text = f.read().replace("\n", "")
        f.close()

        try:
            self.validate_script(script_text)
        except Exception:
            return False

        return True


__sem_validator = None


def get_semantic_validator():
    global __sem_validator

    if __sem_validator is None:
        __sem_validator = ScriptFormatManager()

    return __sem_validator
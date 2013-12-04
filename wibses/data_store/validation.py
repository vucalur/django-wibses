# -*- coding: UTF-8 -*-
import jsonschema as js_schm_validate
import json
from wibses.data_store import JSON_ATTR_NAME__NAME, JSON_ATTR_NAME__THRESHOLD, JSON_ATTR_NAME__OBLIGATORY, JSON_ATTR_NAME__WEIGHT, JSON_ATTR_NAME__MIN, JSON_ATTR_NAME__LABEL, JSON_ATTR_NAME__TYPE, JSON_ATTR_NAME__ID, JSON_ATTR_NAME__DIC, JSON_ATTR_NAME__PARAMS, JSON_ATTR_NAME__TOKENS, JSON_ATTR_NAME__SLOTS, JSON_ATTR_NAME__SENTENCES, JSON_ATTR_NAME__SYNTHETIC, JSON_ATTR_NAME__ANALYTICAL, JSON_ATTR_NAME__CIRCUMSTANCES
from wibses.data_store.exceptions import ScriptValidationException, NotJsonObjectException

__script_schema = None


def get_schema():
    global __script_schema
    if __script_schema is None:
        dummy = None
#region script params
        __script_params_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__NAME: {"type": "string", "minLength": 1},
                JSON_ATTR_NAME__ID: {"type": "string"}
            },
            "required": [JSON_ATTR_NAME__NAME],
            "additionalProperties": False
        }
#endregion
#region section params
        __section_params_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__THRESHOLD: {"type": "integer"}
            },
            "required": [JSON_ATTR_NAME__THRESHOLD],
            "additionalProperties": True
        }
#endregion
#region sentence params
        __sentence_params_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__OBLIGATORY: {"type": "boolean"},
                JSON_ATTR_NAME__THRESHOLD: {"type": "integer"},
                JSON_ATTR_NAME__NAME: {"type": "string"},
                JSON_ATTR_NAME__WEIGHT: {"type": "number"}
            },
            "required": [JSON_ATTR_NAME__OBLIGATORY, JSON_ATTR_NAME__THRESHOLD,
                         JSON_ATTR_NAME__NAME, JSON_ATTR_NAME__WEIGHT],
            "additionalProperties": True
        }

#endregion
#region slot params
        __slot_params_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__OBLIGATORY: {"type": "boolean"},
                JSON_ATTR_NAME__MIN: {"type": "integer"},
                JSON_ATTR_NAME__NAME: {"type": "string"},
                JSON_ATTR_NAME__WEIGHT: {"type": "number"}
            },
            "required": [JSON_ATTR_NAME__NAME, JSON_ATTR_NAME__MIN,
                         JSON_ATTR_NAME__OBLIGATORY, JSON_ATTR_NAME__WEIGHT],
            "additionalProperties": True
        }
#endregion
#region token
        __token_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__LABEL: {"type": "string"},
                JSON_ATTR_NAME__TYPE: {"type": "string", "enum": ["token", "quotation"]},
                JSON_ATTR_NAME__ID: {"type": "string"},
                JSON_ATTR_NAME__DIC: {"type": "string"}
            },
            "additionalProperties": False,
            "required": [JSON_ATTR_NAME__LABEL, JSON_ATTR_NAME__TYPE,
                         JSON_ATTR_NAME__ID, JSON_ATTR_NAME__DIC]
        }
#endregion
#region slot
        __slot_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__PARAMS: __slot_params_schema,
                JSON_ATTR_NAME__TOKENS: {
                    "type": "array",
                    "minItems": 1,
                    "items": __token_schema
                }
            },
            "additionalProperties": False,
            "required": [JSON_ATTR_NAME__TOKENS, JSON_ATTR_NAME__PARAMS]
        }
#endregion
#region sentence
        __sentence_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__PARAMS: __sentence_params_schema,
                JSON_ATTR_NAME__SLOTS: {
                    "type": "array",
                    "minItems": 1,
                    "items": __slot_schema
                }
            },
            "additionalProperties": False,
            "required": [JSON_ATTR_NAME__SLOTS, JSON_ATTR_NAME__PARAMS]
        }
#endregion
#region syntethic section
        __syntethic_section_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__PARAMS: __section_params_schema,
                JSON_ATTR_NAME__SENTENCES: {
                    "type": "array",
                    "items": __sentence_schema,
                    "minItems": 1,
                    "maxItems": 1
                }
            },
            "additionalProperties": False,
            "required": [JSON_ATTR_NAME__SENTENCES, JSON_ATTR_NAME__PARAMS]
        }
#endregion
#region analytical section
        __analytical_section_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__PARAMS: __section_params_schema,
                JSON_ATTR_NAME__SENTENCES: {
                    "type": "array",
                    "items": __sentence_schema,
                    "minItems": 1,
                }
            },
            "additionalProperties": False,
            "required": [JSON_ATTR_NAME__SENTENCES, JSON_ATTR_NAME__PARAMS]
        }
#endregion
#region circumstances section
        __circumstances_section_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__PARAMS: __section_params_schema,
                JSON_ATTR_NAME__SENTENCES: {
                    "type": "array",
                    "items": __sentence_schema,
                    "minItems": 1,
                }
            },
            "additionalProperties": False,
            "required": [JSON_ATTR_NAME__SENTENCES, JSON_ATTR_NAME__PARAMS]
        }
#endregion
#region general script schema
        __script_schema = {
            "type": "object",
            "properties": {
                JSON_ATTR_NAME__PARAMS: __script_params_schema,
                JSON_ATTR_NAME__SYNTHETIC: __syntethic_section_schema,
                JSON_ATTR_NAME__ANALYTICAL: __analytical_section_schema,
                JSON_ATTR_NAME__CIRCUMSTANCES: __circumstances_section_schema
            },
            "additionalProperties": False,
            "required": [JSON_ATTR_NAME__PARAMS, JSON_ATTR_NAME__SYNTHETIC,
                         JSON_ATTR_NAME__ANALYTICAL, JSON_ATTR_NAME__CIRCUMSTANCES]
        }
#endregion

    return __script_schema


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


class SemanticScriptValidator:
    def __init__(self):
        self._validator = js_schm_validate.Draft4Validator(get_schema())

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
        __sem_validator = SemanticScriptValidator()

    return __sem_validator
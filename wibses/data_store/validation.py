# -*- coding: UTF-8 -*-
import jsonschema as js_schm_validate
import json
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
                "name": {"type": "string"}
            },
            "required": ["name"],
            "additionalProperties": False
        }
#endregion
#region section params
        __section_params_schema = {
            "type": "object",
            "properties": {
                "threshold": {"type": "integer"}
            },
            "required": ["threshold"],
            "additionalProperties": True
        }
#endregion
#region sentence params
        __sentence_params_schema = {
            "type": "object",
            "properties": {
                "obligatory": {"type": "boolean"},
                "threshold": {"type": "integer"},
                "name": {"type": "string"},
                "weight": {"type": "number"}
            },
            "required": ["obligatory", "threshold", "name", "weight"],
            "additionalProperties": True
        }

#endregion
#region slot params
        __slot_params_schema = {
            "type": "object",
            "properties": {
                "obligatory": {"type": "boolean"},
                "min": {"type": "integer"},
                "name": {"type": "string"},
                "weight": {"type": "number"}
            },
            "required": ["name", "min", "obligatory", "weight"],
            "additionalProperties": True
        }
#endregion
#region token
        __token_schema = {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "type": {"type": "string", "enum": ["token", "quotation"]},
                "id": {"type": "string"},
                "dic": {"type": "string"}
            },
            "additionalProperties": False,
            "required": ["label", "type", "id", "dic"]
        }
#endregion
#region slot
        __slot_schema = {
            "type": "object",
            "properties": {
                "params": __slot_params_schema,
                "tokens": {
                    "type": "array",
                    "minItems": 1,
                    "items": __token_schema
                }
            },
            "additionalProperties": False,
            "required": ["tokens", "params"]
        }
#endregion
#region sentence
        __sentence_schema = {
            "type": "object",
            "properties": {
                "params": __sentence_params_schema,
                "slots": {
                    "type": "array",
                    "minItems": 1,
                    "items": __slot_schema
                }
            },
            "additionalProperties": False,
            "required": ["slots", "params"]
        }
#endregion
#region syntethic section
        __syntethic_section_schema = {
            "type": "object",
            "properties": {
                "params": __section_params_schema,
                "sentences": {
                    "type": "array",
                    "items": __sentence_schema,
                    "minItems": 1,
                    "maxItems": 1
                }
            },
            "additionalProperties": False,
            "required": ["sentences", "params"]
        }
#endregion
#region analytical section
        __analytical_section_schema = {
            "type": "object",
            "properties": {
                "params": __section_params_schema,
                "sentences": {
                    "type": "array",
                    "items": __sentence_schema,
                    "minItems": 1,
                }
            },
            "additionalProperties": False,
            "required": ["sentences", "params"]
        }
#endregion
#region circumstances section
        __circumstances_section_schema = {
            "type": "object",
            "properties": {
                "params": __section_params_schema,
                "sentences": {
                    "type": "array",
                    "items": __sentence_schema,
                    "minItems": 1,
                }
            },
            "additionalProperties": False,
            "required": ["sentences", "params"]
        }
#endregion
#region general script schema
        __script_schema = {
            "type": "object",
            "properties": {
                "params": __script_params_schema,
                "synthetic": __syntethic_section_schema,
                "analytical": __analytical_section_schema,
                "circumstances": __circumstances_section_schema
            },
            "additionalProperties": False,
            "required": ["params", "synthetic", "analytical", "circumstances"]
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

    def validate_script_text(self, json_text):
        try:
            json_obj = json.loads(json_text)
        except Exception:
            raise NotJsonObjectException(json_text)

        errors = sorted(self._validator.iter_errors(json_obj), key=lambda e: e.path)
        if len(errors) == 0:
            return True

        errors_wrappers = []
        for err in errors:
            errors_wrappers.append(ScriptValidationError(err))

        raise ScriptValidationException(errors_wrappers)

    def validate_script_file(self, file_path):
        f = open(file_path, "r")
        script_text = f.read().replace("\n", "")
        f.close()

        try:
            self.validate_script_text(script_text)
        except Exception:
            return False

        return True


__sem_validator = None


def get_semantic_validator():
    global __sem_validator

    if __sem_validator is None:
        __sem_validator = SemanticScriptValidator()

    return __sem_validator
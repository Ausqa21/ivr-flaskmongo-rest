from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError


user_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
        "balance": {
            "type": "number"
        },
        "number": {
            "type": "string",
            "pattern": "^[0-9]{10}$"
        },
        "passcode": {
            "type": "string",
            "pattern": "^[0-9]{4}$"
        }
    },
    "additionalProperties": False
}


def validate_user_data(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {"ok": True, "data": data}

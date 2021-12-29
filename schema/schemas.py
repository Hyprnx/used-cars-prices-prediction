SCHEMA_CONTACTS = {
    "type": "object",
    "properties": {
        'name': {
            "type": "string"
        },
        'phone_number':{
            'type': 'string'
        },
        'address':{
            'type': 'string'
        }
    },
    "required": [
        "name",
        "phone_number"
    ]
}

SCHEMA_USED_CARS = {
    "type": "object",
    "properties": {
        'name': {
            "type": "string"
        },
        "id": {
            "type": "string"
        },
        "source": {
            "type": "string"
        },
        "source_url": {
            "type": "string"
        },
        "contacts": SCHEMA_CONTACTS
    },
    "required": [
        "id",
        "name",
        "source",
        "source_url",
        "contacts"
    ]
}
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
        "contacts": SCHEMA_CONTACTS,
        'origin':{
            'type': 'string'
        },
        'km_driven':{
            'type': 'number'
        },
        'internal_color':{
            'type': 'string'
        },
        'external_color': {
            'type': 'string'
        },
        'seats':{
            'type': 'integer'
        },
        'engine_capacity':{
            'type': 'number'
        },
        'fuel':{
            'type': 'string'
        #    Gasoline or Diesel
        },
        'transmission': {
            'type': 'string'
        #    Manual or Automatic
        },
        'wheel_drive':{
            'type': 'string'
        },
        'price':{
            'type': 'number'
        },
        'year': {
            'type': 'number'
        },

    },
    "required": [
        "name",
        "source_url",
        "origin",
        "km_driven",
        "external_color",
        "seats",
        "engine_capacity",
        "fuel",
        "transmission",
        "wheel_drive",
        "price",
        "year"
    ]
}
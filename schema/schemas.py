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
            'type': 'string',
            'pattern': 'import|domestic'
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
            'type': 'number'
        },
        'engine_capacity':{
            'type': 'number'
        },
        'fuels':{
            'type': 'string',
            'pattern': 'gasoline|diesel|hybrid|electric'
        #    Gasoline, Diesel, Hybrid or Electric
        },
        'transmission': {
            'type': 'string',
            'pattern': 'automatic|manual'
        #    Manual or Automatic
        },
        'wheel_drive':{
            'type': 'string',
            'pattern': 'FWD|RWD|AWD|4WD'
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
        # "origin",
        # "km_driven",
        # "external_color",
        "seats",
        # "engine_capacity",
        # "fuels",
        "transmission",
        "wheel_drive",
        "price",
        # "year"
    ],
    'additionalProperties': False
}
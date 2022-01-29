SCHEMA_CONTACTS = {
    "type": "object",
    "properties": {
        'name': {
            "type": "string"
        },
        'phone_number': {
            'type': 'string'
        },
        'address': {
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
        'brand': {
            "type": "string"
        },
        'model': {
            "type": "string"
        },
        'type': {
            "type": "string",
            'pattern': 'suv|sedan|coupe|crossover|hatchback|convertible|cuv|pickup|van|wagon'
            #     minivan = van
            #     pickup = bán tải
            #     CUV = Crossover
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
        'origin': {
            'type': 'string',
            'pattern': 'import|domestic'
        },
        'km_driven': {
            'type': 'number'
        },
        'internal_color': {
            'type': 'string'
        },
        'external_color': {
            'type': 'string'
        },
        'seats': {
            'type': 'number'
        },
        'engine_capacity': {
            'type': 'number'
        },
        'fuels': {
            'type': 'string',
            'pattern': 'gasoline|diesel|hybrid|electric'
        },
        'transmission': {
            'type': 'string',
            'pattern': 'automatic|manual'
        },
        'wheel_drive': {
            'type': 'string',
            'pattern': 'FWD|RWD|AWD|4WD'
        },
        'price': {
            'type': 'number'
        },
        'year': {
            'type': 'number'
        },

    },
    "required": [
        "name",
        "brand"
        "source_url",
        "type",
        "origin",
        "km_driven",
        "external_color",
        "seats",
        "fuels",
        "transmission",
        "price",
        "year"
    ],
    'additionalProperties': False
}


SCHEMA_USED_CARS_FINAL = {
    "type": "object",
    "properties": {
        'name': {
            "type": "string"
        },
        'brand': {
            "type": "string"
        },
        'model': {
            "type": "string"
        },
        'type': {
            "type": "string",
            'pattern': 'suv|sedan|coupe|crossover|hatchback|convertible|cuv|pickup|van|wagon'
            #     minivan = van
            #     pickup = bán tải
            #     CUV = Crossover
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
        'origin': {
            'type': 'string',
            'pattern': 'import|domestic'
        },
        'km_driven': {
            'type': 'number'
        },
        'internal_color': {
            'type': 'string'
        },
        'external_color': {
            'type': 'string'
        },
        'seats': {
            'type': 'number'
        },
        'engine_capacity': {
            'type': 'number'
        },
        'fuels': {
            'type': 'string',
            'pattern': 'gasoline|diesel|hybrid|electric'
        },
        'transmission': {
            'type': 'string',
            'pattern': 'automatic|manual'
        },
        'wheel_drive': {
            'type': 'string',
            'pattern': 'FWD|RWD|AWD|4WD'
        },
        'price': {
            'type': 'number'
        },
        'year': {
            'type': 'number'
        },

    },
    "required": [
        "name",
        "brand",
        "source_url",
        "type",
        "origin",
        "km_driven",
        "external_color",
        "seats",
        "engine_capacity",
        "fuels",
        "transmission",
        "wheel_drive",
        "price",
        "year"
    ],
    'additionalProperties': False
}


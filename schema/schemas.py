#  Copyright 2022. Nguyen Thanh Tuan, To Duc Anh, Tran Minh Khoa, Duong Thu Phuong, Nguyen Anh Tu, Kieu Son Tung, Nguyen Son Tung
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from schema.schemas import SCHEMA_USED_CARS

from base import BaseClass

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.ERROR)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Validator(BaseClass):
    SCHEMA = None

    def __init__(self):
        super().__init__()

    def validate(self, entry):
        try:
            self.log.info('Validating %s' %entry)
            validate(instance=entry, schema=self.SCHEMA)
            self.log.info('Entry validated: passed')
            return True, "OK"
        except ValidationError as e:
            return False, e.message


class ValidateUsedCars(Validator):
    SCHEMA = SCHEMA_USED_CARS

    def __init__(self):
        super().__init__()


def main():
    seller = {
        'name': 'To Duc Anh',
        'phone_number': '0123456789',
    }

    cars_sample = {
            "name": "toyota vios 1 5g 2010",
            "source_url": "https://bonbanh.com/xe-toyota-vios-1.5g-2010-3996371",
            "origin": "domestic",
            "km_driven": 12000,
            "external_color": "Bạc",
            "internal_color": "Đen",
            "seats": 4,
            "fuels": "gasoline",
            "engine_capacity": 1.5,
            "transmission": "automatic",
            "wheel_drive": "FWD",
            "price": 290000000,
            "year": 2010,
            "type": "sedan",
            "brand": "toyota"
    }

    validator = ValidateUsedCars()
    print('Validate used car result:', validator.validate(cars_sample))


if __name__ == '__main__':
    main()

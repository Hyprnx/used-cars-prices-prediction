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
        'name': 'Ford Mustang',
        "id": "ford_mustang",
        "source": "https://bonbanh.com",
        "source_url": 'https://bonbanh.com/xe-mercedes_benz-c_class-c200-2016-4163071',
        "contacts": seller,
        'transmission': 'automatic',
        'price': 123456789,
        'wheel_drive': 'FWD',
        'seats': 4
    }

    validator = ValidateUsedCars()
    print('Validate used car result:', validator.validate(cars_sample))


if __name__ == '__main__':
    main()

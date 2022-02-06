import json
from schema.validate import ValidateUsedCars


path = '/Users/minhkhoa/Documents/used-cars-prices-prediction/data/sanxehot/sanxehot_detail.json'
validator = ValidateUsedCars()

with open(path) as f:
    d = json.load(f)

for i in d:
    print(validator.validate(i))






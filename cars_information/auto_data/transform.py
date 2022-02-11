import json
from pprint import pprint

cars = []
for line in open('cars_information/auto_data/car_database.json', 'r', encoding='utf8'):
    cars.append(json.loads(line))

ensure_keys = []
for i in cars:
    for key in i.keys():
        ensure_keys.append(key)

keys = set(ensure_keys)

for i in keys:
    print(i)

print(len(keys))
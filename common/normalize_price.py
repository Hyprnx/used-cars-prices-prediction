def replace_all(replacer, value):
    for old, new in replacer.items():
        value = value.replace(old, new)
    return value


def normalize_price(price):
    billion = {'Tỷ': '1000000000',
               'tỷ': '1000000000',
               'Tỉ': '1000000000',
               'tỉ': '1000000000'}
    million = {'Triệu': '1000000',
               'triệu': '1000000'}

    price = replace_all(billion, price)
    price = replace_all(million, price)
    price = price.split(' ')
    price = [i for i in price if i]
    price = [int(i) for i in price]
    try:
        price = price[0] * price[1] + price[2] * price[3]
    except IndexError:
        price = price[0] * price[1]
    return price

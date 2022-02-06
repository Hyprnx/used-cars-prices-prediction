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
    print(price)
    price = [(float(i)) for i in price]
    try:
        price = price[0] * price[1] + price[2] * price[3]
    except IndexError:
        price = price[0] * price[1]
    return int(price)

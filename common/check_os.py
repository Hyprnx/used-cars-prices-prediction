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

import platform

def get_operating_system():
    return platform.system()

def get_architecture():
    architecture = platform.architecture()
    if architecture == '32bit':
        raise Warning('Only Windows support 32 bits webdriver')
    return architecture

def get_selenium_chrome_webdriver_path(defined_path=None):
    if defined_path:
        return defined_path

    operating_system = get_operating_system()
    # Linux: Linux
    # Mac: Darwin
    # Windows: Windows

    architecture = get_architecture()
    if operating_system == 'Linux':
        chrome_driver_path = 'webdriver/chromedriver_linux'
    elif operating_system == 'Darwin':
        if platform.processor() == 'i386':
            chrome_driver_path = 'webdriver/chromedriver_mac64'
        elif platform.processor() == 'arm':
            chrome_driver_path = 'webdriver/chromedriver_mac64_m1'
        else:
            raise OSError('Your Operating System is not supported')
    elif operating_system == 'Windows':
        chrome_driver_path = 'webdriver/chromedriver_win_32.exe'
    else:
        raise OSError('Your Operating System is not supported')

    return chrome_driver_path

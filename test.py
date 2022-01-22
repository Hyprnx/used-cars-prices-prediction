import re

string = 'B C D'

pattern = re.compile('A')

if pattern.findall(string):
    print('True')
else:
    print('False')

HEADER_NOTE = '\n{0:^5}| {1:^100}| {2:^30}\n{3:-^150s}'.format('id','note','tags','-')
HEADER_BOOK = '\n{0:^14}| {1:^30}| {2:^30}| {3:^30}| {4:^10}\n{5:-^150s}'.format('name','phones','email','address','birthday','-')

SEPARATOR = '\n{0:-^150s}'.format('-')

class colors:
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    END = '\x1b[0m'

def wrap(string, width):
    return [string[i:i + width] for i in range(0, len(string), width)]

def splitted_text(text):
    result = []
    for i in range(len(text)):
        if len(text[i]) < 100:
            result.append('\n{0:5}| {1:100}| {2:30}'.format('', text[i],''))
        else:
            result.append('\n{0:5}| {1:109}| {2:30}'.format('', text[i],''))
    return result
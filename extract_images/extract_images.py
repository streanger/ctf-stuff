import sys
import os
import time
import re
import string
import base64


def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def read_bin(file):
    with open(file, "rb") as f:
        data = f.read()
    return data
    
    
def write_bin(file, data):
    with open(file, 'wb') as f:
        f.write(data)
        f.close()
    return True
    
    
def simple_read(file):
    with open(file, 'r') as f:
        data = f.read().splitlines()
        f.close()
    return data
    
    
def find_indexes(sub, s):
    indexes = [m.start() for m in re.finditer(sub, s)]
    return indexes
    
    
def remove_sub(sub, s):
    index = s.find(sub)
    number = len(sub)
    return s[:index] + s[index+number:]
    
    
if __name__ == "__main__":
    script_path()
    data = read_bin('file.pdf')
    start = bytes([int(item, 16) for item in '89 50 4E 47 0D 0A 1A 0A'.split()])
    stop = bytes([int(item, 16) for item in '49 45 4E 44 AE 42 60 82'.split()])
    
    converted = data
    startIndexes = find_indexes(start, data)
    stopIndexexs = find_indexes(stop, data)
    out = list(zip(startIndexes, stopIndexexs))
    for key, (begin, end) in enumerate(out):
        img = data[begin:end+8]
        converted = remove_sub(img, converted)
        # print(img)
        file = "{}.png".format(key)
        write_bin(file, img)
    write_bin('pdf_ok.pdf', converted)
    
    
    
    
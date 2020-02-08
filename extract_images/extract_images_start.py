import sys
import os
import time
import re
import string
import base64


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def read_bin(file):
    with open(file, 'rb') as f:
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
    data = read_bin('Legend.gif')
    jfif_bytes_string = 'FF D8 FF E0 00 10 4A 46 49 46 00 01' # JPEG raw or in the JFIF or Exif file format
    start = bytes([int(item, 16) for item in jfif_bytes_string.split()])
    
    
    # converted = data
    start_indexes = find_indexes(start, data)
    stop_indexes = [(item-1) for item in start_indexes[1:]] + [len(data)]
    pairs = list(zip(start_indexes, stop_indexes))
    
    for key, (stop, start) in enumerate(pairs):
        img = data[stop:start]
        file = "img_{:02}.jpg".format(key)
        write_bin(file, img)
        
        
'''
gif magic numbers:
47 49 46 38 37 61       GIF87a
47 49 46 38 39 61       GIF89a

'''






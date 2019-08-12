'''this script looks for magic headers hidden into files'''
import sys
import os
import re
import struct
import zlib
import time
from juster import justify
import pprint


def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def calc_len(data):
    return struct.unpack('>i', data)[0]
    
    
def calc_crc32(data):
    ''' https://stackoverflow.com/questions/30092226/how-to-calculate-crc32-with-python-to-match-online-results/30092294 '''
    return (zlib.crc32(data) & 0xffffffff).to_bytes(4, 'big')
    
    
def write_bin(file, data):
    with open(file, 'wb') as f:
        f.write(data)
        f.close()
    return True
    
    
def read_bin(file):
    with open(file, "rb") as f:
        data = f.read()
    return data
    
    
def simple_read(file):
    with open(file, 'r') as f:
        data = f.read()
        f.close()
    return data
    
    
def simple_write(file, data):
    '''simple_write data to .txt file, with specified data'''
    with open(file, "w") as f:
        f.write(str(data) + "\n")
        f.close()
    return True

    
def find_files_headers(data, filters):
    '''filters is list of files headers'''
    return True
    
    
def headers_formats():
    data ={
        'Excel': [208, 207, 17, 224],
        'Linux_bin': [127, 69, 76, 70],
        'OFT': [79, 70, 84, 50],
        'PDF': [37, 80, 68, 70],
        'PPT': [208, 207, 17, 224],
        'Word': [208, 207, 17, 224],
        'ani': [82, 73, 70, 70],
        'au': [46, 115, 110, 100],
        'bmp_01': [66, 77, 248, 169],
        'bmp_02': [66, 77, 98, 37],
        'bmp_03': [66, 77, 118, 3],
        'cab': [77, 83, 67, 70],
        'dll': [77, 90, 144, 0],
        'exe_01': [77, 90, 80, 0],
        'exe_02': [77, 90, 144, 0],
        'flv': [70, 76, 86, 1],
        'gif_01': [71, 73, 70, 56, 57, 97],
        'gif_02': [71, 73, 70, 56, 55, 97],
        'gz': [31, 139, 8, 8],
        'ico': [0, 0, 1, 0],
        'jpeg_01': [255, 216, 255, 225],
        'jpeg_02': [255, 216, 255, 224],
        'jpeg_03': [255, 216, 255, 254],
        'mp3_01': [73, 68, 51, 46],
        'mp3_02': [73, 68, 51, 3],
        'msi': [208, 207, 17, 224],
        'png': [137, 80, 78, 71],
        'rar': [82, 97, 114, 33],
        'sfw_01': [67, 87, 83, 6],
        'sfw_02': [67, 87, 83, 8],
        'tar': [31, 139, 8, 0],
        'tgz': [31, 157, 144, 112],
        'wmv': [48, 38, 178, 117],
        'zip': [80, 75, 3, 4],
        'docx': [0x50, 0x4B, 0x03, 0x04, 0x14, 0x00, 0x06, 0x00],
        'txt': [0x0D, 0x0A]}
    return data
    
    
def create_dictio():
    formats = [line.split(' ', 1) for line in simple_read('formats.txt').splitlines()]
    # dictio = {key : [hex(int(item, 16)) for item in value.split()] for key, value in formats} # this returns hexstring
    dictio = {key : [int(item, 16) for item in value.split()] for key, value in formats}
    pprint.pprint(dictio)
    return dictio
    
    
if __name__ == "__main__":
    script_path()
    
    headers = headers_formats()
    files = [file for file in os.listdir() if file.endswith(('.png', '.jpg', '.zip'))]
    for file in files:
        print('file: {}, detected formats:'.format(file))
        data = read_bin(file)
        for index, (key, value) in enumerate(headers.items()):
            
            # this is for all indexes
            if False:
                s = ''.join([chr(item) for item in value])
                indexes = [m.start() for m in re.finditer(bytes(s, 'utf-8'), data)]
                if indexes:
                    for c in indexes:
                        print('\t', data[c-10:c+10])
                        
            # THIS IS ONLY 1st POSITION! 
            pos = data.find(bytearray(value))
            if pos > -1:
                print(key, pos)
        print('\n')

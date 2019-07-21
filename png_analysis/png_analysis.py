import sys
import os
import re
import struct
import zlib
import time
from juster import justify


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
    
    
def simple_write(file, data):
    '''simple_write data to .txt file, with specified data'''
    with open(file, "w") as f:
        f.write(str(data) + "\n")
        f.close()
    return True
    
    
def iter_indexes(data, indexes):
    return [data[indexes[key-1]:index] for key, index in enumerate(indexes) if key]
    
    
def png_info(file):
    ''' 
    return info about png chunks in str format. Think of making class of it 
    -------------------------------------------------------------
    PNG BUILDING:
        chunk1 --> lenght, 4 bytes
        chunk2 --> tag(IHDR, IDAT...), 4 bytes
        chunk3 --> data, lenght specified in chunk1
        chunk4 --> CRC32 calculated from chunk2 and chunk3
    -------------------------------------------------------------
    '''
    with open(file, "rb") as f:
        bytesData = f.read()
        
    pngStart = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    if not bytesData.startswith(pngStart):
        return False
        
    tagsNames = ['IHDR', 'IDAT', 'IEND']
    tags = {tag: bytes(tag, 'utf-8') for tag in tagsNames}
    chunksIndexes = []
    for tag, value in tags.items():
        chunksIndexes.extend([(tag, m.start()) for m in re.finditer(value, bytesData)])
    chunksIndexes.sort(key=lambda tup: tup[1])
    
    chunksData = [['TAG', 'INDEX', 'LENGHT', 'DATA', 'CRC32VALUE', 'CRC32CALCULATED', 'CRC32_EQUAL']]
    for tag, index in chunksIndexes:
        lenght = calc_len(bytesData[index-4:index])                         # chunk 1
        data = bytesData[index+4:index+4+lenght]                            # chunk 3
        crc32Value = bytesData[index+4+lenght:index+4+lenght+4]             # chunk 4
        crc32Calculated = calc_crc32(tags[tag] + data)                      # crc32_equal
        # we append len(data) instead of data, which is not possible to put into table
        chunksData.append([tag, index, lenght, len(data), crc32Value, crc32Calculated, crc32Value==crc32Calculated])
    return chunksData
    
    
if __name__ == "__main__":
    script_path()
    
    files = ["death.png", "bonsai.png", "tree.png"]
    for file in files:
        # ************ get info about chunks ************
        chunksData = png_info(file)
        info = justify(chunksData, grid=False, frame=True, header=True, enumerator=True, topbar='PNG ANALYSIS RESULTS --> {}'.format(file))
        # print(info)
        simple_write(file.split('.')[0] + '.txt', info)

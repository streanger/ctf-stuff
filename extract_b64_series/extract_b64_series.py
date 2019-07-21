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
    
    
def timer(func):
    def f(*args, **kwargs):
        before = time.time()
        val = func(*args, **kwargs)
        after = time.time()
        print("func: {}, elapsed time: {}s".format(func.__name__, after-before))
        return val
    return f
    
    
def read_bin(file):
    with open(file, "rb") as f:
        data = f.read()
    return data
    
    
def decode_base64(coded_string):
    out = base64.b64decode(coded_string)
    return out
    
    
@timer
def extract_series(data):
    '''
        -find series of base64 encoded data in bytes 
        -with using regex
        -example of data:
            data = b'thisis53=dd=d23=3===443=**=ss=++/24+==__*&*(very__SDA+th===ing_*(%$#now'
        -alphabet, just for info:
            alphabet = (string.ascii_letters + string.digits + '+/').encode('utf-8')
    '''
    regex = re.compile(b'[a-zA-Z0-9+/]+={0,2}')               # seems to work properly
    parts = re.findall(regex, data)
    parts = [item for item in parts if not len(item)%4]     # filter part for len == 4 at least
    return parts
    

@timer
def extract_series__(data):
    '''
        -find series of base64 encoded data in bytes 
        -this is very ugly for now :(
        -maybe need some regex
    '''
    alphabet = (string.ascii_letters + string.digits + '+/' + '=').encode('utf-8')  # + '=' is not correct, but need to use for now
    parts = []
    part = b''
    for key, value in enumerate(data):
        if value in alphabet:
            if value.to_bytes(1, 'big') == b'=':
                if not part:
                    # can't start with '='
                    continue
            if part and part[-1].to_bytes(1, 'big') == b'=' and (value.to_bytes(1, 'big') == b'='):
                # when two last elements are '=='
                part += value.to_bytes(1, 'big')
                parts.append(part)
                part = b''
                continue
                
            if part and (part[-1].to_bytes(1, 'big') == b'=') and not (value.to_bytes(1, 'big') == b'='):
                # when last element is '=' and current is not '='
                parts.append(part)
                part = value.to_bytes(1, 'big')
                continue
            
            part += value.to_bytes(1, 'big')
        else:
            if part:
                parts.append(part)
                part = b''
    if part:
        parts.append(part)
        part = b''
        
    # print('before filter: {}'.format(len(parts)))
    parts = [item for item in parts if not len(item)%4]     # filter part for len == 4 at least
    # print('after filter: {}'.format(len(parts)))
    return parts
    
    
if __name__ == "__main__":
    script_path()
    file = 'death.png'
    data = read_bin(file)
    parts1 = extract_series(data)
    parts2 = extract_series__(data)
    
    print(len(parts1))
    print(len(parts2))
    
    
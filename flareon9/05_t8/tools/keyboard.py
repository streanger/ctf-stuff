import sys
import time
import binascii
import pyautogui
from rich import print

"""
useful:
    https://pyautogui.readthedocs.io/en/latest/keyboard.html
    
"""

def chars_to_hexstring(chars):
    return binascii.hexlify(bytes(chars, 'utf-8')).decode('utf-8')
    
    
if __name__ == "__main__":
    base1 = 'TdQdBRa1nxGU06dbB27E7SQ7TJ2+cd7zstLXRQcLbmh2nTvDm1p5IfT/Cu0JxShk6tHQBRWwPlo9zA1dISfslkLgGDs41WK12ibWIflqLE4Yq3OYIEnLNjwVHrjL2U4Lu3ms+HQc4nfMWXPgcOHb4fhokk93/AJd5GTuC5z+4YsmgRh1Z90yinLBKB+fmGUyagT6gon/KHmJdvAOQ8nAnl8K/0XG+8zYQbZRwgY6tHvvpfyn9OXCyuct5/cOi8KWgALvVHQWafrp8qB/JtT+t5zmnezQlp3zPL4sj2CJfcUTK5copbZCyHexVD4jJN+LezJEtrDXP1DJNg=='
    base2 = 'F1KFlZbNGuKQxrTD/ORwudM8S8kKiL5F906YlR8TKd8XrKPeDYZ0HouiBamyQf9/Ns7u3C2UEMLoCA0B8EuZp1FpwnedVjPSdZFjkieYqWzKA7up+LYe9B4dmAUM2lYkmBSqPJYT6nEg27n3X656MMOxNIHt0HsOD0d+'
    
    payload1 = 'y.d.N.8.B.X.q.1.6.R.E.=.'
    payload1 = payload1.replace('.', '\x00')
    payload2 = 'V.Y.B.U.p.Z.d.G.'
    payload2 = payload2.replace('.', '\x00')
    
    hexstring = chars_to_hexstring(payload2)
    hexstring_space = ' '.join([hexstring[n:n+2] for n in range(0, len(hexstring), 2)])
    print(hexstring_space)
    input('start typing ')
    time.sleep(5)
    pyautogui.write(hexstring, interval=0.05)
    
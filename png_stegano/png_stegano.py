import sys
import os
import cv2
import numpy as np


def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def get_stegano(layer, bit):
    ''' extract image hidden in some bits '''
    ones = create_ones_image(layer.shape, bit)
    bit_and = cv2.bitwise_and(ones, layer)
    return bit_and
    
    
def create_ones_image(shape, bit):
    ''' create image for bitwise operation '''
    ones = np.ones(shape, dtype=np.uint8)*(2**bit)
    return ones
    
    
def extract_all_layers(img, dir):
    ''' it should work for all layers (R, G, B, alpha)
        think of returning images, instead of saving inside, like its now
    '''
    currentPath = script_path()
    if not os.path.exists(dir):
        os.makedirs(dir)
    newPath = os.path.join(currentPath, dir)
    
    layers = cv2.split(img)
    for key, layer in enumerate(layers):
        fullBits = [get_stegano(layer, bit) for bit in range(8)]
        for bit, item in enumerate(fullBits):
            out = os.path.join(newPath, 'layer_{}_bit_{}.png'.format(key, bit))
            cv2.imwrite(out, item)
            print('image: {} created'.format(out))
    return True
    
    
def create_hidden_image(file):
    ''' example of how to create hidden image '''
    # file = 'view_02.png'
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    shape = img.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # create two subimages as example
    one = create_ones_image(shape, 0)
    cv2.putText(one, 'OpenCV_one', (10, 75), font, 2, (1), 2, cv2.LINE_AA)
    
    two = create_ones_image(shape, 1)
    cv2.putText(one, 'OpenCV_two', (10, 125), font, 2, (2), 2, cv2.LINE_AA)
    
    hidden = one + two
    hidden = np.dstack((hidden, hidden, hidden))
    
    # now we need to clear 3 bits in img
    clear = create_ones_image(shape, 0)*248
    clear = np.dstack((clear, clear, clear))
    img = cv2.bitwise_and(clear, img)
    
    # when hidden image is created, and img is "cleared", we can combine two images into one
    out = hidden + img
    return out
    
    
if __name__ == "__main__":
    script_path()
    
    # create hidden image
    fileIn = 'view_02.png'
    out = create_hidden_image(fileIn)
    show_image('out', out)
    cv2.imwrite('out.png', out)
    
    # extract layers
    fileOut = 'out.png'
    img = cv2.imread(fileOut, cv2.IMREAD_UNCHANGED)
    extract_all_layers(img, fileOut.split('.')[0])
    
'''
todo:
    -make some example with true hidden image (+)
    -make function, to join hidden image into normal (8 single bits, to one) (+-)
    -
    
'''

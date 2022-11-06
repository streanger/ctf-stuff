import cv2


if __name__ == "__main__":
    img129 = cv2.imread('129.bmp') 
    img133 = cv2.imread('133.bmp') 
    out = img129 ^ img133
    cv2.imwrite('out.png', out)
    
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import os

data = []

with open(r'python\data.txt', 'r') as db:
    array = db.readline()
    for i in range(1, 287):
        array = db.readline()
        array = eval(array)
        data.append(array)

num_arr = np.array(data)
image = np.uint8(num_arr)
# cv2.imshow('asd', image)
# cv2.waitKey()
# cv2.destroyAllWindows()

directory = r'fingerprintTemp'
os.chdir(directory)
cv2.imwrite('temp.jpg', image)
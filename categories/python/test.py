# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:17:56 2020

@author: Admin
"""
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import os
import time

data = []

with open(r'dataContainer.php', 'r') as db:
    for i in range(0, 286):
        array = []
        packet = db.readline()
        if not packet:
            break
        #print(packet)
        arr_packet = packet.split()
        for i in range(0, 32):
            x = int(arr_packet[i])
            array_temp = []
            while(x != 0):
                temp = x%2
                x = x//2
                array_temp.append(temp)
            length = 8 - len(array_temp)
            while(length != 0):
                array_temp.append(0)
                length -= 1
            for j in range (7, -1, -1):
                array.append(array_temp[j])
        data.append(array)

num_arr = np.array(data)
num_arr = (num_arr == 1).astype(np.uint8)
num_arr = 255*num_arr
#image = np.uint8(num_arr)
# cv2.imshow('asd', num_arr)
# cv2.waitKey()
# cv2.destroyAllWindows()

directory = r'fingerprint'
os.chdir(directory)
cv2.imwrite('temp' + str(time.time()) + '.jpg', num_arr)
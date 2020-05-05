# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:37:54 2020

@author: Admin
"""


import cv2
import numpy as np
import os
from skimage.morphology import convex_hull_image, erosion
import math

def matchingFingerprint(template_fg, input_fg):
    template_corePoint = template_fg[0]
    input_corePoint = input_fg[0]
    template_len = len(template_fg)
    input_len = len(input_fg)
    diff_x = input_corePoint[0] - template_corePoint[0]
    diff_y = input_corePoint[1] - template_corePoint[1]
    score = 0
    for i in range(1, input_len):
        point = input_fg[i]
        x = point[0] - diff_x
        y = point[1] - diff_y
        if(x < 0 or y < 0):
            continue
        for j in range(1, template_len):
            match_point = template_fg[j]
            if(match_point[3] == point[3]):
                sd = np.sqrt((x - match_point[0])**2 + (y - match_point[1])**2)
                if(sd <= 8):
                    score += 1
                    break    
    
    score = score*2/(template_len + input_len)
    
    return score

# def matchingFingerprint(template_fg, input_fg):
#     template_corePoint = template_fg[0]
#     input_corePoint = input_fg[0]
#     template_len = len(template_fg)
#     input_len = len(input_fg)
#     diff_x = input_corePoint[0] - template_corePoint[0]
#     diff_y = input_corePoint[1] - template_corePoint[1]
#     diff_o = input_corePoint[2] - template_corePoint[2]
#     match_list = []
#     for i in range(1, input_len):
#         match_tuple = (i,)
#         point = input_fg[i]
#         x = point[0] - diff_x
#         y = point[1] - diff_y
#         if(x < 0 or y < 0):
#             continue
#         for j in range(1, template_len):
#             match_point = template_fg[j]
#             if(match_point[3] == point[3]):
#                 sd = np.sqrt((x - match_point[0])**2 + (y - match_point[1])**2)
#                 if(sd <= 6):
#                     match_tuple += (j,)
#         if(len(match_tuple) > 1):            
#             match_list.append(match_tuple)
    
#     score = len(match_list)
#     score = score*2/(template_len + input_len)
#     return (match_list, score)

# def matchingFingerprint(template_fg, input_fg):
#     template_corePoint = template_fg[0]
#     input_corePoint = input_fg[0]
#     template_len = len(template_fg)
#     input_len = len(input_fg)
#     diff_x = input_corePoint[0] - template_corePoint[0]
#     diff_y = input_corePoint[1] - template_corePoint[1]
#     diff_o = input_corePoint[2] - template_corePoint[2]
#     match_list = []
#     for i in range(1, input_len):
#         match_tuple = (i,)
#         point = input_fg[i]
#         x = point[0] - diff_x - template_corePoint[0]
#         y = point[1] - diff_y - template_corePoint[1]
#         x_prime = math.cos(diff_o)*x - math.sin(diff_o)*y + template_corePoint[0]
#         y_prime = math.sin(diff_o)*x + math.cos(diff_o)*y + template_corePoint[1]
#         o_prime = point[2] - diff_o
#         if(x_prime < 0 or y_prime < 0):
#             continue
#         for j in range(1, template_len):
#             match_point = template_fg[j]
#             if(match_point[3] == point[3]):
#                 sd = np.sqrt((x_prime - match_point[0])**2 + (y_prime - match_point[1])**2)
#                 dd = min(abs(match_point[2] - o_prime), (math.pi - abs(match_point[2] - o_prime)))
#                 # if(sd <= 6 and dd < math.pi/18):
#                 if(sd <= 6):
#                     match_tuple += (j,)
                    
#         if(len(match_tuple) > 1):            
#             match_list.append(match_tuple)
    
#     score = len(match_list)
#     score = score*2/(template_len + input_len)
#     return (match_list, score)

with open('python\database_db2.txt', 'r') as rdb:
    with open('python\database_db2_input.txt', 'r') as idb:
        # user_id = rdb.readline()
        # minutiaeList = eval(rdb.readline())
        
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # matchList, score = matchingFingerprint(minutiaeList, inputList)
        # print(matchList)
        # print(score)

        input_id = idb.readline()
        inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # input_id = idb.readline()
        # inputList = eval(idb.readline())

        for i in range(0, 9):

            user_id = rdb.readline()

            minutiaeList = eval(rdb.readline())
            score = matchingFingerprint(minutiaeList, inputList)
            print(score)

        
# data = (
#         '\xEF\x01\xFF\xFF\xFF\xFF\x02\x00\x82\x03\x01\x5F\x25\x00\x00\xFE'
#         '\x3E\xFC\x02\xF8\x02\xF0\x00\xF0\x00\xF0\x00\xE0\x00\xE0\x00\xE0'
#         '\x00\xE0\x00\xE0\x00\xE0\x00\xE0\x00\xE0\x00\xE0\x00\xE0\x00\xE0' 
#         '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' 
#         '\x00\x64\x11\xE4\xFE\x6C\xA0\xA6\xBE\x25\x23\x67\xDE\x3C\xAA\xD1' 
#         '\x3E\x71\xAF\x67\x9E\x3B\x3F\xE7\x9E\x3D\x0B\x50\x7F\x58\x34\x51' 
#         '\x7F\x27\xBB\xA6\xFF\x24\x41\xD0\x5F\x59\x08\x63\x94\x5C\x0B\xA5'
#         '\x9C\x33\x39\x67\xBC\x73\x13\xE4\x75\x74\x10\x4C\x7A\x2B\x1B\xCF'
#         '\x32\x38\xB1\xD1\x3A\x36\xBC\x11\x1A\x2F\xBB\xEF\x01\xFF\xFF\xFF'
#         '\xFF\x02\x00\x82\x33\x8E\x27\x7B\x6C\x0C\x4E\x18\x35\x11\x10\x72'
#         '\x32\x12\xE6\xF2\x38\x1E\x8E\xF8\x3C\x35\x51\x78\x28\x1E\x66\xD3'
#         '\x33\xA2\xE6\x99\x40\x35\xE7\xF9\x6E\x8D\xE2\xF6\x2C\x34\xD1\x70'
#         '\x34\x16\xE6\x34\x3B\x96\xCF\x8E\x40\x25\x26\xB4\x32\x2F\xA7\xD4'
#         '\x36\x24\x8F\xF2\x28\x36\x91\xCD\x26\x2E\xEB\x50\x26\x31\x14\xB1' 
#         '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' 
#         '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' 
#         )

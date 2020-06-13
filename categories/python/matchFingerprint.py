# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:37:54 2020

@author: Admin
"""


import cv2
import numpy as np
import os
import math

def matchingFingerprint(template_fg, input_fg):
    template_corePoint = template_fg[0]
    input_corePoint = input_fg[0]
    template_len = len(template_fg)
    input_len = len(input_fg)
    diff_x = input_corePoint[0] - template_corePoint[0]
    diff_y = input_corePoint[1] - template_corePoint[1]
    score = 0
    numberOfMatchingInTemplate = np.zeros(template_len, dtype = int)
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
                dd = min(abs(match_point[2] - point[2]), (math.pi - abs(match_point[2] - point[2])))
                if(sd <= 35 and dd < math.pi/24):
                    if(numberOfMatchingInTemplate[j] < 2):
                        numberOfMatchingInTemplate[j] += 1
                        score += 1
                        break
    
    score = score*2/(template_len + input_len - 2)
    
    return score

def matchingFingerprint2(template_fg, input_fg):
    template_len = len(template_fg)
    input_len = len(input_fg)
    score = 0
    for i in range(1, input_len):
        point = input_fg[i]
        for j in range(1, template_len):
            match_point = template_fg[j]
            if(match_point[3] == point[3]):
                sd = np.sqrt((point[0] - match_point[0])**2 + (point[1] - match_point[1])**2)
                dd = min(abs(match_point[2] - point[2]), (math.pi - abs(match_point[2] - point[2])))
                if(sd <= 20 and dd < math.pi/18):
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

threshold = 0.2
with open('../fingerprintData/fingerpint_db.txt', 'r') as rdb: # file txt database
    with open('../fingerprintData/temp.txt', 'r') as idb: # file txt chua du lieu cua van tay can so khop
        # user_id = rdb.readline()
        # minutiaeList = eval(rdb.readline())
        
        # input_id = idb.readline()
        # inputList = eval(idb.readline())
        # matchList, score = matchingFingerprint(minutiaeList, inputList)
        # print(matchList)
        # print(score)
        
      #  input_id = idb.readline()
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
        highest_score = -1
        highest_id = ''
        isMatch = False
        while(1):
            user_id = rdb.readline()
            if not user_id:
                break
            minutiaeList = rdb.readline()
            if not minutiaeList:
                break
            minutiaeList = eval(minutiaeList)
            score = matchingFingerprint(minutiaeList, inputList)
            if(score >= threshold and highest_score < score):
                isMatch = True
                highest_id = user_id
                highest_score = score

           # print(score)
        if(isMatch):
            print('1-' + highest_id)
        else:
            print('2-0')


        

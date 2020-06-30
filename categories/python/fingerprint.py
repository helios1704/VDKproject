# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 08:39:34 2020

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:04:52 2020

@author: Admin
"""


# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import cv2
import numpy as np
import skimage
from skimage.morphology import skeletonize
from enhanced import image_enhance, ridge_orient
import math

 
BORDER_DISTANCE = 15

def faultMinutiae(minutiae, mask):
    (x, y) = minutiae[0:2]
    (x_mask, y_mask) = mask.shape
    
    score = 500
    score_temp = 0
    (x_temp, y_temp) = (x, y)
    #################################
    while(x_temp >= 0):
        if(mask[x_temp][y]):
            score_temp += 1
            x_temp -= 1
        else:
            break
    if(score_temp < score):
        score = score_temp
    ###################################
    x_temp = x
    score_temp = 0
    while(x_temp < x_mask):
        if(mask[x_temp][y]):
            score_temp += 1
            x_temp += 1
        else:
            break
    if(score_temp < score):
        score = score_temp
    ######################################
    score_temp = 0    
    while(y_temp >= 0):
        if(mask[x][y_temp]):
            score_temp += 1
            y_temp -= 1
        else:
            break
    if(score_temp < score):
        score = score_temp
    #######################################    
    score_temp = 0    
    y_temp = y
    while(y_temp < y_mask):
        if(mask[x][y_temp]):
            score_temp += 1
            y_temp += 1
        else:
            break
    if(score_temp < score):
        score = score_temp
    #####################################
    if(score < BORDER_DISTANCE):
        return True
    else:
        return False
    
def extractMinutiae(img, orientim, mask):
    
    DIST = findRidgeWidth(img)
    
    # extract minutiae
    rows, cols = img.shape
    minutiaeList = []
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if(img[i][j] == 1):
                listPoints = [img[i-1][j-1], img[i-1][j], img[i-1][j+1], img[i][j+1], img[i+1][j+1], img[i+1][j], img[i+1][j-1], img[i][j-1], img[i-1][j-1]]
                CN = 0
                for k in range(0, 8):
                    if(listPoints[k] != listPoints[k+1]):
                        CN = CN + 1
                CN = CN / 2
                if(CN == 1):
                    temp_minutiae = (i, j, orientim[i][j], 1)
                    if(not faultMinutiae(temp_minutiae, mask)):
                        minutiaeList.append(temp_minutiae)
                elif(CN == 3):
                    temp_minutiae = (i, j, orientim[i][j], 3)
                    if(not faultMinutiae(temp_minutiae, mask)):
                        minutiaeList.append(temp_minutiae)         
    
    # remove false minutiae    
    ####### time 1 ##################
    numPoints = len(minutiaeList)
   
    # x_min = x_max = minutiaeList[0][0]
    # y_min = y_max = minutiaeList[0][1]
    # for i in range(1, numPoints):
    #     if(x_min > minutiaeList[i][0]):
    #         x_min = minutiaeList[i][0]
    #     if(x_max < minutiaeList[i][0]):
    #         x_max = minutiaeList[i][0]
    #     if(y_min > minutiaeList[i][1]):
    #         y_min = minutiaeList[i][1]
    #     if(y_max < minutiaeList[i][1]):
    #         y_max = minutiaeList[i][1]
    
    # center = ((x_min + x_max)//2, (int)(y_min + y_max)//2, 0, 0)
    
    
    markFaultMinutiae = np.zeros(numPoints, dtype = int)

    for i in range(0, numPoints - 1):
        if(markFaultMinutiae[i]):
            continue
        for j in range(i + 1, numPoints):
            if(markFaultMinutiae[j]):
                continue
            (X1, Y1) = minutiaeList[i][0:2]
            (X2, Y2) = minutiaeList[j][0:2]
            distance = np.sqrt((X2-X1)**2 + (Y2-Y1)**2)
            if(distance < DIST):
                markFaultMinutiae[i] = 1
                markFaultMinutiae[j] = 1
                # SpuriousMin.append(i)
                # SpuriousMin.append(j)
                
    newMinutiaeGroup = []          
    for i in range(0, numPoints):
        if(not markFaultMinutiae[i]):
            newMinutiaeGroup.append(minutiaeList[i])
       
    return newMinutiaeGroup
                     
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
                if(sd <= 25 and dd <= math.pi/24):
                    if(numberOfMatchingInTemplate[j] < 2):
                        numberOfMatchingInTemplate[j] += 1
                        score += 1
                        break    
    
    # print(score)
    score = score*2/(template_len + input_len - 2)
    # print(numberOfMatchingInTemplate)
    # print(sum(numberOfMatchingInTemplate))
    return score
       
def blockImage(orientim):
    r, c = orientim.shape
    rows = r//3
    cols = c//3
    newImg = np.zeros((rows, cols))
    for i in range(0, rows):
        for j in range(0, cols):
            x = i*3
            y = j*3
            sums = orientim[x][y] + orientim[x][y+1] + orientim[x][y+2] + orientim[x+1][y] + orientim[x+1][y+1] + orientim[x+1][y+2] + orientim[x+2][y] + orientim[x+2][y+1] + orientim[x+2][y+2]
            sums = sums/9
            newImg[i][j] = sums
    return newImg

def detectCorePoint(or_im):
    orientim = blockImage(or_im)
    rows, cols = orientim.shape
    core = ()
    cons_min = 500
    for i in range(2, rows - 2):
        for j in range(2, cols - 2):
            # listR = [orientim[i-2][j]*180/math.pi, orientim[i-2][j-1]*180/math.pi, orientim[i-2][j-2]*180/math.pi, orientim[i-1][j-2]*180/math.pi,
            #          orientim[i][j-2]*180/math.pi, orientim[i+1][j-2]*180/math.pi, orientim[i+2][j-2]*180/math.pi, orientim[i+2][j-1]*180/math.pi,
            #          orientim[i+2][j]*180/math.pi, orientim[i+2][j+1]*180/math.pi, orientim[i+2][j+2]*180/math.pi, orientim[i+1][j+2]*180/math.pi,
            #          orientim[i][j+2]*180/math.pi, orientim[i-1][j+2]*180/math.pi, orientim[i-2][j+2]*180/math.pi, orientim[i-2][j+1]*180/math.pi]
            
            listR = [orientim[i-2][j]*180/math.pi, orientim[i-2][j+1]*180/math.pi, orientim[i-2][j+2]*180/math.pi, orientim[i-1][j+2]*180/math.pi,
                     orientim[i][j+2]*180/math.pi, orientim[i+1][j+2]*180/math.pi, orientim[i+2][j+2]*180/math.pi, orientim[i+2][j-1]*180/math.pi,
                     orientim[i+2][j]*180/math.pi, orientim[i+2][j-1]*180/math.pi, orientim[i+2][j-2]*180/math.pi, orientim[i+1][j-2]*180/math.pi,
                     orientim[i][j-2]*180/math.pi, orientim[i-1][j-2]*180/math.pi, orientim[i-2][j-2]*180/math.pi, orientim[i-2][j-1]*180/math.pi]
            A = 0
            if((listR[0] >= 0 and listR[0] < 50) or (listR[0] >= 120 and listR[0] < 180)):
                A += 1
            if(listR[1] >= 0 and listR[1] < 80):
                A += 1
            if(listR[2] >= 15 and listR[2] < 90):
                A += 1
            if(listR[3] >= 15 and listR[3] < 95):
                A += 1
            if(listR[4] >= 15 and listR[4] < 100):
                A += 1
            if(listR[5] >= 20 and listR[5] < 120):
                A += 1
            if(listR[6] >= 20 and listR[6] < 115):
                A += 1
            if(listR[7] >= 25 and listR[7] < 125):
                A += 1
            if(listR[8] >= 40 and listR[8] < 140):
                A += 1
            if(listR[9] >= 40 and listR[9] < 150):
                A += 1
            if(listR[10] >= 40 and listR[10] < 160):
                A += 1
            if(listR[11] >= 40 and listR[11] < 165):
                A += 1
            if(listR[12] >= 60 and listR[12] < 175):
                A += 1
            if(listR[13] >= 100 and listR[13] < 180):
                A += 1
            if(listR[14] >= 122 and listR[14] < 180):
                A += 1
            if((listR[15] >= 120 and listR[15] < 180) or (listR[15] >=0 and listR[15] < 40)):
                A += 1
            
            if(A >= 15):
                sum_cos = sum_sin = 0
                for k in range(0, 16):
                    angle = listR[k]*math.pi/90
                    sum_cos += math.cos(angle)
                    sum_sin += math.sin(angle)
                cons = math.sqrt(sum_cos**2 + sum_sin**2)/16     
                if(cons_min > cons):
                    cons_min = cons
                    core = (i, j)
    
    
    if(len(core) == 0):
        cons_min = 500
        g_x, g_y = np.gradient(orientim)
        G = np.zeros(orientim.shape)
        for i in range(0, rows):
            for j in range(0, cols):
                G[i][j] = math.sqrt(g_x[i][j]**2 + g_y[i][j]**2)
        for i in range(2, rows - 2):
            for j in range(2, cols - 2):
                if(orientim[i][j] > 2.15 and (G[i][j] >= 0.55 and G[i][j] <= 1.75)):
                    listR = [orientim[i-2][j], orientim[i-2][j+1], orientim[i-2][j+2], orientim[i-1][j+2],
                             orientim[i][j+2], orientim[i+1][j+2], orientim[i+2][j+2], orientim[i+2][j-1],
                             orientim[i+2][j], orientim[i+2][j-1], orientim[i+2][j-2], orientim[i+1][j-2],
                             orientim[i][j-2], orientim[i-1][j-2], orientim[i-2][j-2], orientim[i-2][j-1]]
                    sum_cos = sum_sin = 0
                    for k in range(0, 16):
                        angle = 2*listR[k]
                        sum_cos += math.cos(angle)
                        sum_sin += math.sin(angle)
                        cons = math.sqrt(sum_cos**2 + sum_sin**2)/16     
                        if(cons_min > cons):
                            cons_min = cons
                            core = (i, j)
        
    if(len(core) == 0):
        core = (0, 0, 0, 0)
    else:
        (x, y) = core
        x = x*3 + 1
        y = y*3 + 1
        core = (x, y, or_im[x][y], 0)
    
    return core
     
def findRidgeWidth(img):
    rows, cols = img.shape
    
    index_row = rows // 2
    imdex_col = cols // 2
    
    ridgeWidth = 0
    ridgeWith_1 = 1
    ridgeWith_2 = 1
    ridgeWith_3 = 1
    
    for i in range(0, cols):
        if img[index_row][i] == 1:
            ridgeWith_1 += 1
        if img[index_row - 30][i] == 1:
            ridgeWith_2 += 1
        if img[index_row + 30][i] == 1:
            ridgeWith_3 += 1
    
    ridgeWidth += rows/ridgeWith_1 + rows/ridgeWith_2 + rows/ridgeWith_3
    
    ridgeWith_1 = 1
    ridgeWith_2 = 1
    ridgeWith_3 = 1
    
    for i in range(0, rows):
        if img[i][imdex_col] == 1:
            ridgeWith_1 += 1
        if img[i][imdex_col - 30] == 1:
            ridgeWith_2 += 1
        if img[i][imdex_col - 30] == 1:
            ridgeWith_3 += 1
    
    ridgeWidth += cols/ridgeWith_1 + cols/ridgeWith_2 + cols/ridgeWith_3
    
    ridgeWidth = ridgeWidth/6
    
    return ridgeWidth
   
def convertToImage():
    data = []

    with open(r'dataContainer.php', 'r') as db:
        for i in range(0,286):
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
    
    return num_arr

######### read fingerprint image ##########   
    


# path = r'C:\Users\Admin\.spyder-py3\enhanced\Fingerprint\tro2\1.jpg'
# img = cv2.imread(path, 0)

################################
# cv2.imshow('original image', img)

img = convertToImage()

# cv2.imshow('original image', img)

############## enhanced image #########################
rows, cols = np.shape(img)
aspect_ratio = np.double(rows)/np.double(cols)
new_rows = 200
new_cols = new_rows/aspect_ratio
img = cv2.resize(img,(np.int(new_cols),np.int(new_rows)))

# cv2.imshow('original image', img)

img1, orientim, mask = image_enhance(img)
img1 = 255*img1
#######################################################


####################################
# cv2.imshow('enhanced image', img1)


################## thining image ############################
ret, img2 = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY)

# cv2.imshow('binary image', img2)

bin_thresh = (img2 == 0).astype(int)


skel = skeletonize(bin_thresh)
#############################################################

# or_im = ridge_orient(skel, 1, 7, 7)

############# extract minutiae and detect core point #########
minutiaeList = extractMinutiae(skel, orientim, mask)
# point, list_core = detectCorePoint(orientim, center)
point = detectCorePoint(orientim)

#############################################################

# final_minutiae_list = []
# final_minutiae_list.append(center)
# length = len(minutiaeList)
# for i in range(0, length):
#     final_minutiae_list.append(minutiaeList[i])


final_minutiae_list = []
final_minutiae_list.append(point)
length = len(minutiaeList)
for i in range(0, length):
    final_minutiae_list.append(minutiaeList[i])


threshold = 0.35
with open('../fingerprintData/fingerpint_db.txt', 'r') as rdb: # file txt database
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
        score1 = matchingFingerprint(minutiaeList, final_minutiae_list)
        score2 = matchingFingerprint(final_minutiae_list, minutiaeList)
        score = (score1 + score2)/2
        if(score >= threshold and highest_score < score):
            isMatch = True
            highest_id = user_id
            highest_score = score

    if(isMatch):
        print('1-' + highest_id)
    else:
        print('2-0')


# print("--- %s seconds ---" % (time.time() - start_time))


# user_id = '000004'
# with open('myDatabase.txt', 'a') as db_f:
#     db_f.write(user_id)
#     db_f.write('\n')
#     db_f.write(str(final_minutiae_list))
#     db_f.write('\n')
    
    
##################################
# skel = (skel == 0).astype(np.uint8)
# skel = 255*skel   
# cv2.imshow('thinning image', skel)


# skel = (skel == 0).astype(int)
    
# numPoints = len(minutiaeList)
# print(numPoints)

# for i in range(0, numPoints):
#     (x, y) = minutiaeList[i][0:2]
#     (rr, cc) = skimage.draw.circle_perimeter(x, y, 3)
#     skel[rr, cc] = 1
# skel = (skel == 0).astype(np.uint8)
# skel = 255*skel


# (x, y) = point[0:2]
# (rr, cc) = skimage.draw.circle_perimeter(x, y, 3)
# skel[rr, cc] = 1
# skel = (skel == 0).astype(np.uint8)
# skel = 255*skel

#ksize = 5
#sigma = 3
#theta = 1*np.pi/4
#lamda = 1*np.pi/4
#gamma = 0.5
#phi = 0
#
#kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, phi, ktype=cv2.CV_32F)
#plt.imshow(kernel)



# cv2.imshow('image test2', skel)


# cv2.waitKey()
# cv2.destroyAllWindows()




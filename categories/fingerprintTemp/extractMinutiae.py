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
from skimage.morphology import skeletonize
import skimage
from enhanced import image_enhance, ridge_orient
import math

def extractMinutiae(img, orientim):
    
    # extract minutiae
    rows, cols = img.shape;
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
                    minutiaeList.append((i, j, orientim[i][j], 1))
                elif(CN == 3):
                    minutiaeList.append((i, j, orientim[i][j], 3))          
    
    # remove false minutiae    
    ####### time 1 ##################
    SpuriousMin = []
    numPoints = len(minutiaeList)
    x_min = x_max = minutiaeList[0][0]
    y_min = y_max = minutiaeList[0][1]
    for i in range(1, numPoints):
        if(x_min > minutiaeList[i][0]):
            x_min = minutiaeList[i][0]
        if(x_max < minutiaeList[i][0]):
            x_max = minutiaeList[i][0]
        if(y_min > minutiaeList[i][1]):
            y_min = minutiaeList[i][1]
        if(y_max < minutiaeList[i][1]):
            y_max = minutiaeList[i][1]
    
    for i in range(0, numPoints):
        x = minutiaeList[i][0]
        y = minutiaeList[i][1]
        if(x - x_min < 10 or x_max - x < 10 or y - y_min < 10 or y_max - y < 10):
            SpuriousMin.append(i)
    
    new = []          
    SpuriousMin = np.unique(SpuriousMin)
    for i in range(0, numPoints):
        if(not i in SpuriousMin):
            new.append(minutiaeList[i])
    ########################################
    
    ###### time 2 ###########
    # SpuriousMin = []
    # numPoints = len(new)
    # x_min = x_max = new[0][0]
    # y_min = y_max = new[0][1]
    # for i in range(1, numPoints):
    #     if(x_min > new[i][0]):
    #         x_min = new[i][0]
    #     if(x_max < new[i][0]):
    #         x_max = new[i][0]
    #     if(y_min > new[i][1]):
    #         y_min = new[i][1]
    #     if(y_max < new[i][1]):
    #         y_max = new[i][1]
    
    # for i in range(0, numPoints):
    #     x = new[i][0]
    #     y = new[i][1]
    #     if(y - y_min < 5 or y_max - y < 5):
    #         SpuriousMin.append(i)
    
    # new2 = []          
    # SpuriousMin = np.unique(SpuriousMin)
    # for i in range(0, numPoints):
    #     if(not i in SpuriousMin):
    #         new2.append(new[i])
    #######################################
    
    
    numPoints = len(new)
    SpuriousMin = []
    for i in range(0, numPoints - 1):
        for j in range(i + 1, numPoints):
            (X1, Y1) = new[i][0:2]
            (X2, Y2) = new[j][0:2]
            distance = np.sqrt((X2-X1)**2 + (Y2-Y1)**2)
            if(distance < 7):
                SpuriousMin.append(i)
                SpuriousMin.append(j)
                
    new1 = []          
    SpuriousMin = np.unique(SpuriousMin)
    for i in range(0, numPoints):
        if(not i in SpuriousMin):
            new1.append(new[i])
    
    numPoints = len(new1)
    x_min = x_max = new1[0][0]
    y_min = y_max = new1[0][1]
    for i in range(1, numPoints):
        if(x_min > new1[i][0]):
            x_min = new1[i][0]
        if(x_max < new1[i][0]):
            x_max = new1[i][0]
        if(y_min > new1[i][1]):
            y_min = new1[i][1]
        if(y_max < new1[i][1]):
            y_max = new1[i][1]
    
    center = ((x_min + x_max)/2 , (y_min + y_max)/2)
    
    return (new1, center)
                     
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
                if(sd <= 10):
                    score += 1
                    break      
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
        
    
    (x, y) = core
    x = x*3 + 1
    y = y*3 + 1
    core = (x, y, or_im[x][y], 0)
    
    return core
     
######### read fingerprint image ##########   
path = r'anh.jpg'
img = cv2.imread(path, 0)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
###########################################


################################
# cv2.imshow('original image', img)


############## enhanced image #########################
rows, cols = np.shape(img)
aspect_ratio = np.double(rows)/np.double(cols)
new_rows = 350
new_cols = new_rows/aspect_ratio
img = cv2.resize(img,(np.int(new_cols),np.int(new_rows)))
img1, orientim, mask = image_enhance(img)
img1 = 255*img1
#######################################################


####################################
# cv2.imshow('enhanced image', img1)


################## thining image ############################
ret, img2 = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY)
bin_thresh = (img2 == 0).astype(int)
skel = skeletonize(bin_thresh)
#############################################################


or_im = ridge_orient(skel, 1, 7, 7)



############# extract minutiae and detect core point #########
minutiaeList, center = extractMinutiae(skel, or_im)
# point, list_core = detectCorePoint(orientim, center)
point = detectCorePoint(or_im)

#############################################################

final_minutiae_list = []
final_minutiae_list.append(point)
length = len(minutiaeList)
for i in range(0, length):
    final_minutiae_list.append(minutiaeList[i])


user_id = '000009'
with open('database_db2_input.txt', 'a') as db_f:
    db_f.write(user_id)
    db_f.write('\n')
    db_f.write(str(final_minutiae_list))
    db_f.write('\n')
    
    
##################################
# skel = (skel == 0).astype(np.uint8)
# skel = 255*skel   
# cv2.imshow('thinning image', skel)


# skel = (skel == 0).astype(int)
numPoints = len(minutiaeList)
print(numPoints)

for i in range(0, numPoints):
    (x, y) = minutiaeList[i][0:2]
    (rr, cc) = skimage.draw.circle_perimeter(x, y, 3)
    skel[rr, cc] = 1
skel = (skel == 0).astype(np.uint8)
skel = 255*skel

# list_num = len(list_point)
# for i in range(0, list_num):
#     (x, y) = list_point[i]
#     (rr, cc) = skimage.draw.circle_perimeter(x, y, 3)
#     skel[rr, cc] = 1
# skel = (skel == 0).astype(np.uint8)
# skel = 255*skel


# (x, y) = point[0:2]
# (rr, cc) = skimage.draw.circle_perimeter(x, y, 3)
# skel[rr, cc] = 1

# (x, y) = point2[0:2]
# (rr, cc) = skimage.draw.circle_perimeter(x, y, 3)
# skel[rr, cc] = 1
# skel = (skel == 0).astype(np.uint8)
# skel = 255*skel   

  
# (x, y) = listCore2
# (rr, cc) = skimage.draw.circle_perimeter(x, y, 3)
# xa[rr, cc] = 0


#ksize = 5
#sigma = 3
#theta = 1*np.pi/4
#lamda = 1*np.pi/4
#gamma = 0.5
#phi = 0
#
#kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, phi, ktype=cv2.CV_32F)
#plt.imshow(kernel)



cv2.imshow('image test3', skel)
# cv2.imshow('im', or_im)
# cv2.imshow('im2', orientim)
# cv2.imshow('im3', xa)
#cv2.imshow('orient img', orientim)
# mask = (mask == 0).astype(np.uint8)
# mask = 255*mask   
# directory = r'C:\Users\Admin\.spyder-py3\enhanced'
# os.chdir(directory)
# cv2.imwrite('2_2.jpg', skel)


cv2.waitKey()
cv2.destroyAllWindows()

#img_name = '1_test.jpg'
#cv2.imwrite('../' + img_name, skel)

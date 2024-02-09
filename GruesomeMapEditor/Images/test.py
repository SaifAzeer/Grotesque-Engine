import os
import numpy as np
import cv2 as cv
im = cv.imread('J:\PythonProg\Pygame\GrotesqueEngine\GruesomeMapEditor\Images\\char_right_anim.png',cv.IMREAD_UNCHANGED)
mask = im[:,:,3]
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(mask, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(im, contours, -1, (0,255,0), 3)
cv.imshow('Contours', im)
i = 0
for c in contours:
    # get the bounding rect
    x, y, w, h = cv.boundingRect(c)
    # to save the images
    cv.imwrite('img_{}.png'.format(i), im[y:y+h,x:x+w])
        
    i += 1
    #if i >= 1000:
    #    break
 
cv.waitKey()
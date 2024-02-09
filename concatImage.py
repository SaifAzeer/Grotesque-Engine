import cv2 
  
# read the images 
img1 = cv2.imread('J:\\Tileset\\Character\\Complete set\\Set 1\\Character with sword and shield\\walk\\walk right1.png', cv2.IMREAD_UNCHANGED) 
img2 = cv2.imread('J:\\Tileset\\Character\\Complete set\\Set 1\\Character with sword and shield\\walk\\walk right2.png', cv2.IMREAD_UNCHANGED)
img3 = cv2.imread('J:\\Tileset\\Character\\Complete set\\Set 1\\Character with sword and shield\\walk\\walk right3.png', cv2.IMREAD_UNCHANGED)
img4 = cv2.imread('J:\\Tileset\\Character\\Complete set\\Set 1\\Character with sword and shield\\walk\\walk right4.png', cv2.IMREAD_UNCHANGED)
im_concat = cv2.hconcat([img1, img1, img3, img4]) 
  
# show the output image 
cv2.imshow( 'J:\\Tileset\\Character\\Complete set\\Set 1\\Character with sword and shield\\walk\\walk_right.png', im_concat) 
cv2.imwrite('J:\\Tileset\\Character\\Complete set\\Set 1\\Character with sword and shield\\walk\\walk_right.png', im_concat) 
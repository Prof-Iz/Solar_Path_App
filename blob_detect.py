import cv2
import os

directory = "C:\\Users\\User\\Desktop"
os.chdir(directory) 

img = cv2.imread("C:\\Users\\User\\Desktop\\skye.jpg",1)

# convert image to grayscale image
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("grey image",gray_image)
# convert the grayscale image to binary image
ret,thresh = cv2.threshold(gray_image,50,255,cv2.CV_8UC1)
# cv2.imshow("Thresh image",thresh)

contours, heirarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
max_countour = contours[0]
for i in range(1,len(contours)):
    if cv2.contourArea(contours[i]) > cv2.contourArea(max_countour):
        max_countour = contours[i]


center, radius = cv2.minEnclosingCircle(max_countour)

center_int = (int(center[0]),int(center[1]))

cv2.circle(img, center_int, 5, (255, 0, 0), -1)
cv2.circle(img, center_int, int(radius), (0, 255, 0),lineType=cv2.LINE_4)

print(center)


# # calculate moments of binary image
# M = cv2.moments(thresh)

# # cv2.imshow("Thresholds",M)
# # calculate x,y coordinate of center
# cX = int(M["m10"] / M["m00"])
# cY = int(M["m01"] / M["m00"])

# # put text and highlight the center
# cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
# cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


# find contours in the binary image




# display the image
# cv2.imshow("Image", img)
cv2.imwrite("Centre_skye.jpg",img)
cv2.waitKey(0)
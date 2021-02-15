import cv2
from PIL import Image
import os

def overlay_graph(route_base,graph):
    '''
    route_base = String Path to image
    graph = image generated of graph at coordinates
    '''

    directory = r'C:\Users\Iz\Desktop\Solar_Path_App\test_pics'
    os.chdir(directory)

    img = cv2.imread(route_base,1)
    
    
    # convert image to grayscale image
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("grey image",gray_image)
    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(gray_image,50,255,cv2.CV_8UC1)
    # cv2.imshow("Thresh image",thresh)
    _,contours,heirarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    max_countour = contours[0]
    for i in range(1,len(contours)):
        if cv2.contourArea(contours[i]) > cv2.contourArea(max_countour):
            max_countour = contours[i]
            
    
    center, radius = cv2.minEnclosingCircle(max_countour)
    
    print(center, radius)
    
    im2 = Image.open(graph)
    
    w, h = im2.size
    
    mf = (radius / 300)
    
    im2_large = im2.resize((int(w * mf),int(h * mf)))
    
    # w, h = im2.size
    w, h = im2_large.size
    
    x_of_graph = int(center[0] - w/2 - 20)
    y_of_graph = int(center[1] - h/2 - 5)

    center_int = (x_of_graph,y_of_graph)

    # cv2.circle(img, center_int, 5, (255, 0, 0), -1)
    # cv2.circle(img, center_int, int(radius), (0, 255, 0),lineType=cv2.LINE_4)

    
    im1 = Image.open(route_base)
    
    
    
    
    
    
    
    im1.paste(im2_large,center_int,mask=im2_large)

    # cv2.imwrite("Centre_skye.jpg",img)
    # im1.save("C:\\Users\\User\\Documents\\GitHub\\Solar_Path_App\\test_pics\\combined.png")
    # cv2.waitKey(0)
    im1.show()
from tkinter import*
import cv2
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import pytesseract as tess
from PIL import Image
import re
import serial
import time
size = 5
import cv2
from PIL import Image
import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import pytesseract
from goprocam import GoProCamera, constants




    
    



pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
c=0

a=0
b=0

# puerto="COM3"
# baudios = 115200

# serialArduino=serial.Serial("COM4",115200)


      
import numpy as np

from pytesseract import Output
import tkinter as tk
from tkinter import Tk, Label, Button
from PIL import ImageTk,Image 

import numpy as np
import sys
import os.path

import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#import serial, time
#arduino=serial.Serial('COM1',9600)
#time.sleep(2) 

#serialArduino=serial.Serial("COM4",115200)
canvaA=0
canvaC=0
canvaB=0
cam = cv2.VideoCapture(1)
coso=0

img_counter = 0

    
def myClick():
    ret, frame = cam.read()
    img_counter =  0
    hello=""+a.get()
    myLabel=Label(root,text=hello)
    #myLabel=Label(root,text=e.get())                                 
    myLabel.place(x=1000, y=100)
    

    
    
    
    
    
   
    
    
    
def video_stream():
    img_counter =  0
    ret, frame = cam.read()
    img_name = "opencv_frame_11.png".format(img_counter)
    cv2.imwrite(img_name, frame)
   
    frame=cv2.resize(frame,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream) 
    
   
while True:
    
    image=cv2.imread("opencv_frame_11.png")
    
    
    texta1=pytesseract.image_to_string(image,config="--psm 11")
  
    
    root = Tk()  
    if(texta1.find("Joint 1 Adjustment")>=0):
        canvaA=1
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        the=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        gray=cv2.blur(gray,(3,3))
        canny=cv2.Canny(gray,0,200)
        #canny=cv2.dilate(canny,None,iterations=1)
        
        cnts,cnts1=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image,cnts,171,(0,255,0),2)
        
        
        for c in cnts:
            area=cv2.contourArea(c)
            x,y,w,h=cv2.boundingRect(c)
            epsilon=0.09*cv2.arcLength(c,True)
           
            approx=cv2.approxPolyDP(c,epsilon,True)
            if len(approx)<=2.5 and area>2000 and area<2100:
                print ("area=",area)
                
                cv2.drawContours(image,[c],0,(0,255,0),2)
                aspect_ratio=float(w)/h
                if aspect_ratio>2.4:
                    placa=image[y:y+h,x:x+w]
                    cv2.imwrite("placaA.png", placa) 
        DEBUG = 0
    
    
        # Determine pixel intensity
        # Apparently human eyes register colors differently.
        # TVs use this formula to determine
        # pixel intensity = 0.30R + 0.59G + 0.11B
        def ii(xx, yy):
            global img, img_y, img_x
            if yy >= img_y or xx >= img_x:
                #print "pixel out of bounds ("+str(y)+","+str(x)+")"
                return 0
            pixel = img[yy][xx]
            return 0.30 * pixel[2] + 0.59 * pixel[1] + 0.11 * pixel[0]
        
        
        # A quick test to check whether the contour is
        # a connected shape
        def connected(contour):
            first = contour[0][0]
            last = contour[len(contour) - 1][0]
            return abs(first[0] - last[0]) <= 1 and abs(first[1] - last[1]) <= 1
        
        
        # Helper function to return a given contour
        def c(index):
            global contours
            return contours[index]
        
        
        # Count the number of real children
        def count_children(index, h_, contour):
            # No children
            if h_[index][2] < 0:
                return 0
            else:
                #If the first child is a contour we care about
                # then count it, otherwise don't
                if keep(c(h_[index][2])):
                    count = 1
                else:
                    count = 0
        
                    # Also count all of the child's siblings and their children
                count += count_siblings(h_[index][2], h_, contour, True)
                return count
        
        
        # Quick check to test if the contour is a child
        def is_child(index, h_):
            return get_parent(index, h_) > 0
        
        
        # Get the first parent of the contour that we care about
        def get_parent(index, h_):
            parent = h_[index][3]
            while not keep(c(parent)) and parent > 0:
                parent = h_[parent][3]
        
            return parent
        
        
        # Count the number of relevant siblings of a contour
        def count_siblings(index, h_, contour, inc_children=False):
            # Include the children if necessary
            if inc_children:
                count = count_children(index, h_, contour)
            else:
                count = 0
        
            # Look ahead
            p_ = h_[index][0]
            while p_ > 0:
                if keep(c(p_)):
                    count += 1
                if inc_children:
                    count += count_children(p_, h_, contour)
                p_ = h_[p_][0]
        
            # Look behind
            n = h_[index][1]
            while n > 0:
                if keep(c(n)):
                    count += 1
                if inc_children:
                    count += count_children(n, h_, contour)
                n = h_[n][1]
            return count
        
        
        # Whether we care about this contour
        def keep(contour):
            return keep_box(contour) and connected(contour)
        
        
        # Whether we should keep the containing box of this
        # contour based on it's shape
        def keep_box(contour):
            xx, yy, w_, h_ = cv2.boundingRect(contour)
        
            # width and height need to be floats
            w_ *= 1.0
            h_ *= 1.0
        
            # Test it's shape - if it's too oblong or tall it's
            # probably not a real character
            if w_ / h_ < 0.1 or w_ / h_ > 10:
                if DEBUG==1:
                    print ("\t Rejected because of shape: (" + str(xx) + "," + str(yy) + "," + str(w_) + "," + str(h_) + ")" + str(w_ / h_))
                          
                return False
            
            # check size of the box
            if ((w_ * h_) > ((img_x * img_y) / 5)) or ((w_ * h_) < 15):
                if DEBUG==1:
                    print ("\t Rejected because of size")
                return False
        
            return True
        
        
        def include_box(index, h_, contour):
            if DEBUG==0:
                print (str(index) + ":")
                if is_child(index, h_):
                    print ("\tIs a child")
                    print ("\tparent " + str(get_parent(index, h_)) + " has " + str(count_children(get_parent(index, h_), h_, contour)) + " children")
                        
                    print( "\thas " + str(count_children(index, h_, contour)) + " children")
        
            if is_child(index, h_) and count_children(get_parent(index, h_), h_, contour) <= 2:
                if DEBUG==0:
                    print ("\t skipping: is an interior to a letter")
                return False
        
            if count_children(index, h_, contour) > 2:
                if DEBUG==0:
                    print ("\t skipping, is a container of letters")
                return False
        
            if DEBUG==0:
                print ("\t keeping")
            return True
        
        # Load the image
        orig_imga = cv2.imread("placaA.png")
        orig_img = cv2.resize(orig_imga, (0,0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Add a border to the image for processing sake
        img = cv2.copyMakeBorder(orig_img, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
        
        # Calculate the width and height of the image
        img_y = len(img)
        img_x = len(img[0])
        
        if DEBUG==0:
            print ("Image is " + str(len(img)) + "x" + str(len(img[0])))
        
        #Split out each channel
        blue, green, red = cv2.split(img)
        
        # Run canny edge detection on each channel
        blue_edges = cv2.Canny(blue, 200, 250)
        green_edges = cv2.Canny(green, 200, 250)
        red_edges = cv2.Canny(red, 200, 250)
        
        # Join edges back into image
        edges = blue_edges | green_edges | red_edges
        
        # Find the contours
        contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        hierarchy = hierarchy[0]
        
        if DEBUG==0:
            processed = edges.copy()
            rejected = edges.copy()
        
        # These are the boxes that we are determining
        keepers = []
        
        # For each contour, find the bounding rectangle and decide
        # if it's one we care about
        for index_, contour_ in enumerate(contours):
            if DEBUG==0:
                print ("Processing #%d" % index_)
        
            x, y, w, h = cv2.boundingRect(contour_)
        
            # Check the contour and it's bounding box
            if keep(contour_) and include_box(index_, hierarchy, contour_):
                # It's a winner!
                keepers.append([contour_, [x, y, w, h]])
                if DEBUG==0:
                    cv2.rectangle(processed, (x, y), (x + w, y + h), (100, 100, 100), 1)
                    cv2.putText(processed, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            else:
                if DEBUG==0:
                    cv2.rectangle(rejected, (x, y), (x + w, y + h), (100, 100, 100), 1)
                    cv2.putText(rejected, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        
        # Make a white copy of our image
        new_image = edges.copy()
        new_image.fill(255)
        boxes = []
        
        # For each box, find the foreground and background intensities
        for index_, (contour_, box) in enumerate(keepers):
        
            # Find the average intensity of the edge pixels to
            # determine the foreground intensity
            fg_int = 0.0
            for p in contour_:
                fg_int += ii(p[0][0], p[0][1])
        
            fg_int /= len(contour_)
            if DEBUG==0:
                print ("FG Intensity for #%d = %d" % (index_, fg_int))
        
            # Find the intensity of three pixels going around the
            # outside of each corner of the bounding box to determine
            # the background intensity
            x_, y_, width, height = box
            bg_int = [
                    # bottom left corner 3 pixels
                    ii(x_ - 1, y_ - 1),
                    ii(x_ - 1, y_),
                    ii(x_, y_ - 1),
        
                    # bottom right corner 3 pixels
                    ii(x_ + width + 1, y_ - 1),
                    ii(x_ + width, y_ - 1),
                    ii(x_ + width + 1, y_),
        
                    # top left corner 3 pixels
                    ii(x_ - 1, y_ + height + 1),
                    ii(x_ - 1, y_ + height),
                    ii(x_, y_ + height + 1),
        
                    # top right corner 3 pixels
                    ii(x_ + width + 1, y_ + height + 1),
                    ii(x_ + width, y_ + height + 1),
                    ii(x_ + width + 1, y_ + height)
                ]
        
            # Find the median of the background
            # pixels determined above
            bg_int = np.median(bg_int)
        
            if DEBUG==0:
                print ("BG Intensity for #%d = %s" % (index_, repr(bg_int)))
        
            # Determine if the box should be inverted
            if fg_int >= bg_int:
                fg = 255
                bg = 0
            else:
                fg = 0
                bg = 255
        
                # Loop through every pixel in the box and color the
                # pixel accordingly
            for x in range(x_, x_ + width):
                for y in range(y_, y_ + height):
                    if y >= img_y or x >= img_x:
                        if DEBUG==0:
                            print ("pixel out of bounds (%d,%d)" % (y, x))
                        continue
                    if ii(x, y) > fg_int:
                        new_image[y][x] = bg
                    else:
                        new_image[y][x] = fg
        
        # blur a bit to improve ocr accuracy
        new_image2 = cv2.blur(new_image, (2,2 ))
        cv2.imwrite("new_imageA.png", new_image2)
        if DEBUG==0:
            cv2.imwrite('edgesA.png', edges)
            cv2.imwrite('processedA.png', processed)
            cv2.imwrite('rejectedA.png', rejected)
        image=cv2.imread("new_imageA.png")
        newImg = cv2.imread("new_imageA.png")
        
        
        gray=cv2.cvtColor(newImg,cv2.COLOR_BGR2GRAY)
        
        gray=cv2.blur(gray,(2,2))
        the=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        canny=cv2.Canny(the,0,200)
        
        
        canny2=cv2.dilate(canny,None,iterations=1)
        
        cnts,cnts1=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image,cnts,171,(0,255,0),2)
        text=pytesseract.image_to_string(newImg,config="--psm 11")
        texta=pytesseract.image_to_string(gray,config="--psm 11")
        textb=pytesseract.image_to_string(canny,config="--psm 11")
        textc=pytesseract.image_to_string(canny2,config="--psm 11")
        #print(text.find("02°"))
        
        b=len(text)
        print(b)
        v1=0
        v2=0
        v3=0
        if(b<=5 and v1==0):
            v1=1
            
        if(b>=6 and v1==0):
            
            print("v1",v1)
            text=text[0:7]
          
        if(b>=5 and v1!=1):
            
            print("v2",v2)
            text=text[0:6]   
          
        if(b>=4 and v2!=1 and v1!=1):
            
            print("v3",v3)
            text=text[0:5] 
           
            
            
        a=text.replace(".","")
        textraf=a.replace("°","")
        
        if(text[0]=="-" and text[2]=="."):
            a1=textraf[0:1]
            a2=textraf[1:3]
            cadenasa1=[a1,"0",a2]
            textraf="".join(cadenasa1)
            print (textraf)  
        if(text[0]!="+" and text[0]!="-"):
            
            cadenasa2=["+",textraf]
            textraf="".join(cadenasa2)
            print ("textra2=",textraf)
            
            if(textraf[0]=="+" and text[1]=="."):
                a3=textraf[0]
                a4=textraf[1:3]
              
                cadenasa3=[a3,"0",a4]
                textraf="".join(cadenasa3)
                print ("textra3=",textraf)  
        print(textraf) 
        
        cadenasf1=["e","S",textraf,"Z"]
        textrafS="".join(cadenasf1)
    if(texta1.find("Joint 2 Adjustment")>=0):
        canvaB=1
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        the=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        gray=cv2.blur(gray,(3,3))
        canny=cv2.Canny(gray,0,200)
        #canny=cv2.dilate(canny,None,iterations=1)
        
        cnts,cnts1=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image,cnts,171,(0,255,0),2)
        
        
        for c in cnts:
            area=cv2.contourArea(c)
            x,y,w,h=cv2.boundingRect(c)
            epsilon=0.09*cv2.arcLength(c,True)
           
            approx=cv2.approxPolyDP(c,epsilon,True)
            if len(approx)<=2.5 and area>2000 and area<2100:
                print ("area=",area)
                
                cv2.drawContours(image,[c],0,(0,255,0),2)
                aspect_ratio=float(w)/h
                if aspect_ratio>2.4:
                    placa=image[y:y+h,x:x+w]
                    cv2.imwrite("placaA.png", placa) 
        DEBUG = 0
    
    
        # Determine pixel intensity
        # Apparently human eyes register colors differently.
        # TVs use this formula to determine
        # pixel intensity = 0.30R + 0.59G + 0.11B
        def ii(xx, yy):
            global img, img_y, img_x
            if yy >= img_y or xx >= img_x:
                #print "pixel out of bounds ("+str(y)+","+str(x)+")"
                return 0
            pixel = img[yy][xx]
            return 0.30 * pixel[2] + 0.59 * pixel[1] + 0.11 * pixel[0]
        
        
        # A quick test to check whether the contour is
        # a connected shape
        def connected(contour):
            first = contour[0][0]
            last = contour[len(contour) - 1][0]
            return abs(first[0] - last[0]) <= 1 and abs(first[1] - last[1]) <= 1
        
        
        # Helper function to return a given contour
        def c(index):
            global contours
            return contours[index]
        
        
        # Count the number of real children
        def count_children(index, h_, contour):
            # No children
            if h_[index][2] < 0:
                return 0
            else:
                #If the first child is a contour we care about
                # then count it, otherwise don't
                if keep(c(h_[index][2])):
                    count = 1
                else:
                    count = 0
        
                    # Also count all of the child's siblings and their children
                count += count_siblings(h_[index][2], h_, contour, True)
                return count
        
        
        # Quick check to test if the contour is a child
        def is_child(index, h_):
            return get_parent(index, h_) > 0
        
        
        # Get the first parent of the contour that we care about
        def get_parent(index, h_):
            parent = h_[index][3]
            while not keep(c(parent)) and parent > 0:
                parent = h_[parent][3]
        
            return parent
        
        
        # Count the number of relevant siblings of a contour
        def count_siblings(index, h_, contour, inc_children=False):
            # Include the children if necessary
            if inc_children:
                count = count_children(index, h_, contour)
            else:
                count = 0
        
            # Look ahead
            p_ = h_[index][0]
            while p_ > 0:
                if keep(c(p_)):
                    count += 1
                if inc_children:
                    count += count_children(p_, h_, contour)
                p_ = h_[p_][0]
        
            # Look behind
            n = h_[index][1]
            while n > 0:
                if keep(c(n)):
                    count += 1
                if inc_children:
                    count += count_children(n, h_, contour)
                n = h_[n][1]
            return count
        
        
        # Whether we care about this contour
        def keep(contour):
            return keep_box(contour) and connected(contour)
        
        
        # Whether we should keep the containing box of this
        # contour based on it's shape
        def keep_box(contour):
            xx, yy, w_, h_ = cv2.boundingRect(contour)
        
            # width and height need to be floats
            w_ *= 1.0
            h_ *= 1.0
        
            # Test it's shape - if it's too oblong or tall it's
            # probably not a real character
            if w_ / h_ < 0.1 or w_ / h_ > 10:
                if DEBUG==1:
                    print ("\t Rejected because of shape: (" + str(xx) + "," + str(yy) + "," + str(w_) + "," + str(h_) + ")" + str(w_ / h_))
                          
                return False
            
            # check size of the box
            if ((w_ * h_) > ((img_x * img_y) / 5)) or ((w_ * h_) < 15):
                if DEBUG==1:
                    print ("\t Rejected because of size")
                return False
        
            return True
        
        
        def include_box(index, h_, contour):
            if DEBUG==0:
                print (str(index) + ":")
                if is_child(index, h_):
                    print ("\tIs a child")
                    print ("\tparent " + str(get_parent(index, h_)) + " has " + str(count_children(get_parent(index, h_), h_, contour)) + " children")
                        
                    print( "\thas " + str(count_children(index, h_, contour)) + " children")
        
            if is_child(index, h_) and count_children(get_parent(index, h_), h_, contour) <= 2:
                if DEBUG==0:
                    print ("\t skipping: is an interior to a letter")
                return False
        
            if count_children(index, h_, contour) > 2:
                if DEBUG==0:
                    print ("\t skipping, is a container of letters")
                return False
        
            if DEBUG==0:
                print ("\t keeping")
            return True
        
        # Load the image
        orig_imga = cv2.imread("placaA.png")
        orig_img = cv2.resize(orig_imga, (0,0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Add a border to the image for processing sake
        img = cv2.copyMakeBorder(orig_img, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
        
        # Calculate the width and height of the image
        img_y = len(img)
        img_x = len(img[0])
        
        if DEBUG==0:
            print ("Image is " + str(len(img)) + "x" + str(len(img[0])))
        
        #Split out each channel
        blue, green, red = cv2.split(img)
        
        # Run canny edge detection on each channel
        blue_edges = cv2.Canny(blue, 200, 250)
        green_edges = cv2.Canny(green, 200, 250)
        red_edges = cv2.Canny(red, 200, 250)
        
        # Join edges back into image
        edges = blue_edges | green_edges | red_edges
        
        # Find the contours
        contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        hierarchy = hierarchy[0]
        
        if DEBUG==0:
            processed = edges.copy()
            rejected = edges.copy()
        
        # These are the boxes that we are determining
        keepers = []
        
        # For each contour, find the bounding rectangle and decide
        # if it's one we care about
        for index_, contour_ in enumerate(contours):
            if DEBUG==0:
                print ("Processing #%d" % index_)
        
            x, y, w, h = cv2.boundingRect(contour_)
        
            # Check the contour and it's bounding box
            if keep(contour_) and include_box(index_, hierarchy, contour_):
                # It's a winner!
                keepers.append([contour_, [x, y, w, h]])
                if DEBUG==0:
                    cv2.rectangle(processed, (x, y), (x + w, y + h), (100, 100, 100), 1)
                    cv2.putText(processed, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            else:
                if DEBUG==0:
                    cv2.rectangle(rejected, (x, y), (x + w, y + h), (100, 100, 100), 1)
                    cv2.putText(rejected, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        
        # Make a white copy of our image
        new_image = edges.copy()
        new_image.fill(255)
        boxes = []
        
        # For each box, find the foreground and background intensities
        for index_, (contour_, box) in enumerate(keepers):
        
            # Find the average intensity of the edge pixels to
            # determine the foreground intensity
            fg_int = 0.0
            for p in contour_:
                fg_int += ii(p[0][0], p[0][1])
        
            fg_int /= len(contour_)
            if DEBUG==0:
                print ("FG Intensity for #%d = %d" % (index_, fg_int))
        
            # Find the intensity of three pixels going around the
            # outside of each corner of the bounding box to determine
            # the background intensity
            x_, y_, width, height = box
            bg_int = [
                    # bottom left corner 3 pixels
                    ii(x_ - 1, y_ - 1),
                    ii(x_ - 1, y_),
                    ii(x_, y_ - 1),
        
                    # bottom right corner 3 pixels
                    ii(x_ + width + 1, y_ - 1),
                    ii(x_ + width, y_ - 1),
                    ii(x_ + width + 1, y_),
        
                    # top left corner 3 pixels
                    ii(x_ - 1, y_ + height + 1),
                    ii(x_ - 1, y_ + height),
                    ii(x_, y_ + height + 1),
        
                    # top right corner 3 pixels
                    ii(x_ + width + 1, y_ + height + 1),
                    ii(x_ + width, y_ + height + 1),
                    ii(x_ + width + 1, y_ + height)
                ]
        
            # Find the median of the background
            # pixels determined above
            bg_int = np.median(bg_int)
        
            if DEBUG==0:
                print ("BG Intensity for #%d = %s" % (index_, repr(bg_int)))
        
            # Determine if the box should be inverted
            if fg_int >= bg_int:
                fg = 255
                bg = 0
            else:
                fg = 0
                bg = 255
        
                # Loop through every pixel in the box and color the
                # pixel accordingly
            for x in range(x_, x_ + width):
                for y in range(y_, y_ + height):
                    if y >= img_y or x >= img_x:
                        if DEBUG==0:
                            print ("pixel out of bounds (%d,%d)" % (y, x))
                        continue
                    if ii(x, y) > fg_int:
                        new_image[y][x] = bg
                    else:
                        new_image[y][x] = fg
        
        # blur a bit to improve ocr accuracy
        new_image2 = cv2.blur(new_image, (2,2 ))
        cv2.imwrite("new_imageA.png", new_image2)
        if DEBUG==0:
            cv2.imwrite('edgesA.png', edges)
            cv2.imwrite('processedA.png', processed)
            cv2.imwrite('rejectedA.png', rejected)
        image=cv2.imread("new_imageA.png")
        newImg = cv2.imread("new_imageA.png")
        
        
        gray=cv2.cvtColor(newImg,cv2.COLOR_BGR2GRAY)
        
        gray=cv2.blur(gray,(2,2))
        the=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        canny=cv2.Canny(the,0,200)
        
        
        canny2=cv2.dilate(canny,None,iterations=1)
        
        cnts,cnts1=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image,cnts,171,(0,255,0),2)
        text=pytesseract.image_to_string(newImg,config="--psm 11")
        texta=pytesseract.image_to_string(gray,config="--psm 11")
        textb=pytesseract.image_to_string(canny,config="--psm 11")
        textc=pytesseract.image_to_string(canny2,config="--psm 11")
        #print(text.find("02°"))
        
        b=len(text)
        print(b)
        v1=0
        v2=0
        v3=0
        if(b<=5 and v1==0):
            v1=1
            
        if(b>=6 and v1==0):
            
            print("v1",v1)
            text=text[0:7]
          
        if(b>=5 and v1!=1):
            
            print("v2",v2)
            text=text[0:6]   
          
        if(b>=4 and v2!=1 and v1!=1):
            
            print("v3",v3)
            text=text[0:5] 
           
            
            
        a=text.replace(".","")
        textraf=a.replace("°","")
        
        if(text[0]=="-" and text[2]=="."):
            a1=textraf[0:1]
            a2=textraf[1:3]
            cadenasa1=[a1,"0",a2]
            textraf="".join(cadenasa1)
            print (textraf)  
        if(text[0]!="+" and text[0]!="-"):
            
            cadenasa2=["+",textraf]
            textraf="".join(cadenasa2)
            print ("textra2=",textraf)
            
            if(textraf[0]=="+" and text[1]=="."):
                a3=textraf[0]
                a4=textraf[1:3]
              
                cadenasa3=[a3,"0",a4]
                textraf="".join(cadenasa3)
                print ("textra3=",textraf)  
        print(textraf) 
        
        cadenasf1=["e","S",textraf,"Z"]
        textrafS="".join(cadenasf1)
        
    if(texta1.find("Joint 3 Adjustment{")>=0):
        canvaC=1
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        the=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        gray=cv2.blur(gray,(3,3))
        canny=cv2.Canny(gray,0,200)
        #canny=cv2.dilate(canny,None,iterations=1)
        
        cnts,cnts1=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image,cnts,171,(0,255,0),2)
        
        
        for c in cnts:
            area=cv2.contourArea(c)
            x,y,w,h=cv2.boundingRect(c)
            epsilon=0.09*cv2.arcLength(c,True)
           
            approx=cv2.approxPolyDP(c,epsilon,True)
            if len(approx)<=2.5 and area>2000 and area<2100:
                print ("area=",area)
                
                cv2.drawContours(image,[c],0,(0,255,0),2)
                aspect_ratio=float(w)/h
                if aspect_ratio>2.4:
                    placa=image[y:y+h,x:x+w]
                    cv2.imwrite("placaA.png", placa) 
        DEBUG = 0
    
    
        # Determine pixel intensity
        # Apparently human eyes register colors differently.
        # TVs use this formula to determine
        # pixel intensity = 0.30R + 0.59G + 0.11B
        def ii(xx, yy):
            global img, img_y, img_x
            if yy >= img_y or xx >= img_x:
                #print "pixel out of bounds ("+str(y)+","+str(x)+")"
                return 0
            pixel = img[yy][xx]
            return 0.30 * pixel[2] + 0.59 * pixel[1] + 0.11 * pixel[0]
        
        
        # A quick test to check whether the contour is
        # a connected shape
        def connected(contour):
            first = contour[0][0]
            last = contour[len(contour) - 1][0]
            return abs(first[0] - last[0]) <= 1 and abs(first[1] - last[1]) <= 1
        
        
        # Helper function to return a given contour
        def c(index):
            global contours
            return contours[index]
        
        
        # Count the number of real children
        def count_children(index, h_, contour):
            # No children
            if h_[index][2] < 0:
                return 0
            else:
                #If the first child is a contour we care about
                # then count it, otherwise don't
                if keep(c(h_[index][2])):
                    count = 1
                else:
                    count = 0
        
                    # Also count all of the child's siblings and their children
                count += count_siblings(h_[index][2], h_, contour, True)
                return count
        
        
        # Quick check to test if the contour is a child
        def is_child(index, h_):
            return get_parent(index, h_) > 0
        
        
        # Get the first parent of the contour that we care about
        def get_parent(index, h_):
            parent = h_[index][3]
            while not keep(c(parent)) and parent > 0:
                parent = h_[parent][3]
        
            return parent
        
        
        # Count the number of relevant siblings of a contour
        def count_siblings(index, h_, contour, inc_children=False):
            # Include the children if necessary
            if inc_children:
                count = count_children(index, h_, contour)
            else:
                count = 0
        
            # Look ahead
            p_ = h_[index][0]
            while p_ > 0:
                if keep(c(p_)):
                    count += 1
                if inc_children:
                    count += count_children(p_, h_, contour)
                p_ = h_[p_][0]
        
            # Look behind
            n = h_[index][1]
            while n > 0:
                if keep(c(n)):
                    count += 1
                if inc_children:
                    count += count_children(n, h_, contour)
                n = h_[n][1]
            return count
        
        
        # Whether we care about this contour
        def keep(contour):
            return keep_box(contour) and connected(contour)
        
        
        # Whether we should keep the containing box of this
        # contour based on it's shape
        def keep_box(contour):
            xx, yy, w_, h_ = cv2.boundingRect(contour)
        
            # width and height need to be floats
            w_ *= 1.0
            h_ *= 1.0
        
            # Test it's shape - if it's too oblong or tall it's
            # probably not a real character
            if w_ / h_ < 0.1 or w_ / h_ > 10:
                if DEBUG==1:
                    print ("\t Rejected because of shape: (" + str(xx) + "," + str(yy) + "," + str(w_) + "," + str(h_) + ")" + str(w_ / h_))
                          
                return False
            
            # check size of the box
            if ((w_ * h_) > ((img_x * img_y) / 5)) or ((w_ * h_) < 15):
                if DEBUG==1:
                    print ("\t Rejected because of size")
                return False
        
            return True
        
        
        def include_box(index, h_, contour):
            if DEBUG==0:
                print (str(index) + ":")
                if is_child(index, h_):
                    print ("\tIs a child")
                    print ("\tparent " + str(get_parent(index, h_)) + " has " + str(count_children(get_parent(index, h_), h_, contour)) + " children")
                        
                    print( "\thas " + str(count_children(index, h_, contour)) + " children")
        
            if is_child(index, h_) and count_children(get_parent(index, h_), h_, contour) <= 2:
                if DEBUG==0:
                    print ("\t skipping: is an interior to a letter")
                return False
        
            if count_children(index, h_, contour) > 2:
                if DEBUG==0:
                    print ("\t skipping, is a container of letters")
                return False
        
            if DEBUG==0:
                print ("\t keeping")
            return True
        
        # Load the image
        orig_imga = cv2.imread("placaA.png")
        orig_img = cv2.resize(orig_imga, (0,0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Add a border to the image for processing sake
        img = cv2.copyMakeBorder(orig_img, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
        
        # Calculate the width and height of the image
        img_y = len(img)
        img_x = len(img[0])
        
        if DEBUG==0:
            print ("Image is " + str(len(img)) + "x" + str(len(img[0])))
        
        #Split out each channel
        blue, green, red = cv2.split(img)
        
        # Run canny edge detection on each channel
        blue_edges = cv2.Canny(blue, 200, 250)
        green_edges = cv2.Canny(green, 200, 250)
        red_edges = cv2.Canny(red, 200, 250)
        
        # Join edges back into image
        edges = blue_edges | green_edges | red_edges
        
        # Find the contours
        contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        hierarchy = hierarchy[0]
        
        if DEBUG==0:
            processed = edges.copy()
            rejected = edges.copy()
        
        # These are the boxes that we are determining
        keepers = []
        
        # For each contour, find the bounding rectangle and decide
        # if it's one we care about
        for index_, contour_ in enumerate(contours):
            if DEBUG==0:
                print ("Processing #%d" % index_)
        
            x, y, w, h = cv2.boundingRect(contour_)
        
            # Check the contour and it's bounding box
            if keep(contour_) and include_box(index_, hierarchy, contour_):
                # It's a winner!
                keepers.append([contour_, [x, y, w, h]])
                if DEBUG==0:
                    cv2.rectangle(processed, (x, y), (x + w, y + h), (100, 100, 100), 1)
                    cv2.putText(processed, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            else:
                if DEBUG==0:
                    cv2.rectangle(rejected, (x, y), (x + w, y + h), (100, 100, 100), 1)
                    cv2.putText(rejected, str(index_), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        
        # Make a white copy of our image
        new_image = edges.copy()
        new_image.fill(255)
        boxes = []
        
        # For each box, find the foreground and background intensities
        for index_, (contour_, box) in enumerate(keepers):
        
            # Find the average intensity of the edge pixels to
            # determine the foreground intensity
            fg_int = 0.0
            for p in contour_:
                fg_int += ii(p[0][0], p[0][1])
        
            fg_int /= len(contour_)
            if DEBUG==0:
                print ("FG Intensity for #%d = %d" % (index_, fg_int))
        
            # Find the intensity of three pixels going around the
            # outside of each corner of the bounding box to determine
            # the background intensity
            x_, y_, width, height = box
            bg_int = [
                    # bottom left corner 3 pixels
                    ii(x_ - 1, y_ - 1),
                    ii(x_ - 1, y_),
                    ii(x_, y_ - 1),
        
                    # bottom right corner 3 pixels
                    ii(x_ + width + 1, y_ - 1),
                    ii(x_ + width, y_ - 1),
                    ii(x_ + width + 1, y_),
        
                    # top left corner 3 pixels
                    ii(x_ - 1, y_ + height + 1),
                    ii(x_ - 1, y_ + height),
                    ii(x_, y_ + height + 1),
        
                    # top right corner 3 pixels
                    ii(x_ + width + 1, y_ + height + 1),
                    ii(x_ + width, y_ + height + 1),
                    ii(x_ + width + 1, y_ + height)
                ]
        
            # Find the median of the background
            # pixels determined above
            bg_int = np.median(bg_int)
        
            if DEBUG==0:
                print ("BG Intensity for #%d = %s" % (index_, repr(bg_int)))
        
            # Determine if the box should be inverted
            if fg_int >= bg_int:
                fg = 255
                bg = 0
            else:
                fg = 0
                bg = 255
        
                # Loop through every pixel in the box and color the
                # pixel accordingly
            for x in range(x_, x_ + width):
                for y in range(y_, y_ + height):
                    if y >= img_y or x >= img_x:
                        if DEBUG==0:
                            print ("pixel out of bounds (%d,%d)" % (y, x))
                        continue
                    if ii(x, y) > fg_int:
                        new_image[y][x] = bg
                    else:
                        new_image[y][x] = fg
        
        # blur a bit to improve ocr accuracy
        new_image2 = cv2.blur(new_image, (2,2 ))
        cv2.imwrite("new_imageA.png", new_image2)
        if DEBUG==0:
            cv2.imwrite('edgesA.png', edges)
            cv2.imwrite('processedA.png', processed)
            cv2.imwrite('rejectedA.png', rejected)
        image=cv2.imread("new_imageA.png")
        newImg = cv2.imread("new_imageA.png")
        
        
        gray=cv2.cvtColor(newImg,cv2.COLOR_BGR2GRAY)
        
        gray=cv2.blur(gray,(2,2))
        the=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        canny=cv2.Canny(the,0,200)
        
        
        canny2=cv2.dilate(canny,None,iterations=1)
        
        cnts,cnts1=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image,cnts,171,(0,255,0),2)
        text=pytesseract.image_to_string(newImg,config="--psm 11")
        texta=pytesseract.image_to_string(gray,config="--psm 11")
        textb=pytesseract.image_to_string(canny,config="--psm 11")
        textc=pytesseract.image_to_string(canny2,config="--psm 11")
        #print(text.find("02°"))
        
        b=len(text)
       
        v1=0
        v2=0
        v3=0
        if(b<=5 and v1==0):
            v1=1
            
        if(b>=6 and v1==0):
            
            print("v1",v1)
            text=text[0:7]
           
        if(b>=5 and v1!=1):
            
            print("v2",v2)
            text=text[0:6]   
          
        if(b>=4 and v2!=1 and v1!=1):
            
            print("v3",v3)
            text=text[0:5] 
           
            
            
        a=text.replace(".","")
        textraf=a.replace("°","")
        
        if(text[0]=="-" and text[2]=="."):
            a1=textraf[0:1]
            a2=textraf[1:3]
            cadenasa1=[a1,"0",a2]
            textraf="".join(cadenasa1)
            print (textraf)  
        if(text[0]!="+" and text[0]!="-"):
            
            cadenasa2=["+",textraf]
            textraf="".join(cadenasa2)
            print ("textra2=",textraf)
            
            if(textraf[0]=="+" and text[1]=="."):
                a3=textraf[0]
                a4=textraf[1:3]
              
                cadenasa3=[a3,"0",a4]
                textraf="".join(cadenasa3)
                print ("textra3=",textraf)  
        print(textraf) 
        
        cadenasf1=["e","S",textraf,"Z"]
        textrafS="".join(cadenasf1)
    
    # ret, frame = cam.read()
    # if not ret:
    #     print("failed to grab frame")
        
    # cv2.imshow('frame', frame)
    # if cv2.waitKey(1) & 0xFF == 27:
        
    #     # ESC pressed
    #     print("Escape hit, closing...")
        
    # elif cv2.waitKey(1) & 0xFF == 32:  
    #     # SPACE pressed
    #     img_name = "opencv_frame_11.png".format(img_counter)
    #     cv2.imwrite(img_name, frame)
    #     print("{} written!".format(img_name))
    #     img_counter += 1 
   
    photo = PhotoImage(file = r"C:\Users\joe\camara5.png")
    photo2 = PhotoImage(file = r"C:\Users\joe\angulo2.png")
    photo3 = PhotoImage(file = r"C:\Users\joe\mov1.png")
    app = Frame(root, bg="white")
    app.grid()
    # Create a label in the frame
    lmain = Label(app)
    lmain.grid(row = 6, column = 0, sticky = W, pady = 500)
   
    #----------------------------------------------------------------------------------------------------------------------------------
    
    
    

    
   
    # if not serialArduino.isOpen():
    #     serialArduino.open()
    # serialArduino.write(textrafS)  
   
     
    
            #serialArduino.flush()
        
    # serialArduino.close()  
        

    canvas = Canvas(root, width = 650, height = 500)  
    canvas2 = Canvas(root, width = 300, height = 300)     
  
    img = ImageTk.PhotoImage(Image.open("epilepsia3.png"))  
    img2 = ImageTk.PhotoImage(Image.open("HUMANA.png"))  
      
    label1 =Label(image=img)
    label1.image = img
    label1.place(x=1, y=50)
    label2=Label(image=img2)
    label2.image = img2
    label2.place(x=500, y=400)
    
    video_stream()
  

    
    #e.pack()  
    a =tk.Entry(root,bg="white",fg="red",width=50)
    a.insert(0,"porcentaje de error es :   ") 
    a.place(x=1400, y=270)
    
    b =tk.Entry(root,bg="white",fg="red",width=50)
    b.insert(0,"porcentaje de error es :   ") 
    b.place(x=1400, y=530)
    
    c =tk.Entry(root,bg="white",fg="red",width=50)
    c.insert(0,"porcentaje de error es :   ") 
    c.place(x=1400, y=720)

    myButton=Button(root, text="Click Me !",image=photo,compound = LEFT,command=myClick)
    myButton.place(x=1400, y=100) 
    
    if(canvaA==0):
        myButton2=Button(root, text="no hay porcentje de error",image=photo2,compound = LEFT)
        myButton2.place(x=1400, y=300) 
    if(canvaA==1):
        myButton2=Button(root, text=textraf,image=photo2,compound = LEFT)
        myButton2.place(x=1400, y=300) 
    
    if(canvaB==0):
        myButton3=Button(root, text="no hay porcentje de error",image=photo2,compound = LEFT)
        myButton3.place(x=1400, y=550) 
    if(canvaB==1):
        myButton3=Button(root, text=textraf,image=photo2,compound = LEFT)
        myButton3.place(x=1400, y=550)
   
    if(canvaC==0):
        myButton3=Button(root, text="no hay porcentje de error",image=photo2,compound = LEFT)
        myButton3.place(x=1400, y=750) 
    if(canvaC==1):
        myButton4=Button(root, text=textraf,image=photo2,compound = LEFT)
        myButton4.place(x=1400, y=750)
    
    #myButton.pack()




    root.mainloop()   
        
    cam.release()             

    cv2.destroyAllWindows()                
    break
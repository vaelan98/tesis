from tkinter import*
import cv2
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import pytesseract as tess

import tkinter as tk
from tkinter import Tk, Label, Button
from PIL import ImageTk,Image 

cam = cv2.VideoCapture(1)
coso=0
tess.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img_counter = 0


def myClick():
    ret, frame = cam.read()
    img_counter =  0
    hello=""+a.get()
    myLabel=Label(root,text=hello)
    #myLabel=Label(root,text=e.get())
    myLabel.place(x=1000, y=100)
    
   
    img_name = "opencv_frame_11.png".format(img_counter)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    img_counter += 1 
    img3 = ImageTk.PhotoImage(Image.open("opencv_frame_11.png"))
    label3=Label(image=img3)
    label3.image = img3
    label3.place(x=700, y=50)
    
   
    
    
    img=Image.open("humana1.png")
    print(pytesseract.image_to_string(img))
   
    img2 = cv2.imread("humana1.png")
    h, w, c = img2.shape
    boxes = pytesseract.image_to_boxes(img2) 
    text = pytesseract.image_to_string(img2) 
    for b in boxes.splitlines():
        b = b.split(" ")
        img4 = cv2.rectangle(img2, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    cv2.imshow("img", img4)
    cv2.waitKey(0)
    print(text)


def video_stream():
    ret, frame = cam.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream) 
    
while True:
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
    root = Tk()  
    photo = PhotoImage(file = r"C:\Users\joe\camara5.png")
    photo2 = PhotoImage(file = r"C:\Users\joe\angulo2.png")
    photo3 = PhotoImage(file = r"C:\Users\joe\mov1.png")
    app = Frame(root, bg="white")
    app.grid()
    # Create a label in the frame
    lmain = Label(app)
    lmain.grid(row = 6, column = 0, sticky = W, pady = 500)
    
    
    
   

   
    
    video_stream()
    
    

    




    root.mainloop()   
        
    cam.release()             

    cv2.destroyAllWindows()                
    break
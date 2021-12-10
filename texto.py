# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 12:44:59 2021

@author: joe
"""


import tkinter as tk
from tkinter import Tk, Label, Button
root=Tk()

#creacion de pantalla
def myClick():
    hello="hello  "+e.get()
    myLabel=Label(root,text=hello)
    #myLabel=Label(root,text=e.get())
    myLabel.pack()
e =tk.Entry(root,bg="white",fg="red",width=50)
e.pack()  
e.insert(0,"enter yout name:   ") 

myButton=Button(root, text="pone nombre jo puta",command=myClick)


myButton.pack()




root.mainloop()
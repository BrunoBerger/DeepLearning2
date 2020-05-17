from tkinter import *
import cv2

master = Tk()
master.minsize(300,100)
master.geometry("320x300")

def callback():
    print("click!")


b = Button(master, text="OK", command=callback)
b.pack()

mainloop()

from tkinter import *
import cv2
import threading

def callbackTest():
    print("click!")

def terminateThread(run_flag):
    print("Attempt Button-Termination")
    run_flag.value = False

def optionWindow(run_flag):
    config = Tk()
    config.title("Options")
    config.minsize(280,300)
    config.maxsize(350,600)
    # Gets the requested values of the height and widht.
    windowWidth = config.winfo_reqwidth()
    windowHeight = config.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(config.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(config.winfo_screenheight()/2 - windowHeight/2)
    # Positions the window in the center of the page.
    config.geometry("+{}+{}".format(positionRight, positionDown))

    b1 = Button(config, text="Print Something",
        command=callbackTest, height=2, width=15)
    b2 = Button(config, text="Terminate Thread",
        command= lambda: terminateThread(run_flag), height=2, width=15)

    b1.place(x = 30, y = 20)
    b2.place(x = 30, y = 70)

    mainloop()

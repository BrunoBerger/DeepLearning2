from tkinter import *
import cv2
import TEST
import threading

def optionWindow(stop_threads):
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


    def callbackTest():
        print("click!")

    def terminateThread():
        stop_threads = True
        print("Attempt Termination")

    b1 = Button(config, text="Print Something", command=callbackTest, height=2, width=15)
    b2 = Button(config, text="Terminate Thread", command=terminateThread, height=2, width=15)

    b1.place(x = 30, y = 20)
    b2.place(x = 30, y = 70)

    mainloop()

if __name__ == '__main__':
    stop_threads = False
    t2 = threading.Thread(target = optionWindow, args =(lambda : stop_threads, ))
    t2.start()
    
    TEST.main(stop_threads)

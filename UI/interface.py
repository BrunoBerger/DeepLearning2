from tkinter import *

from UI import buttonFuncs as bf


def optionWindow(args, run_flag, all_processes):
    # Generate a tkinter window
    config = Tk()
    config.title("Options")
    config.minsize(280,300)
    config.maxsize(280,300)
    # Gets both half the screen width/height and window width/height
    positionRight = int(config.winfo_screenwidth()/1.5)
    positionDown = int(config.winfo_screenheight()/2.5)
    # Positions the window in the center of the page.
    config.geometry("+{}+{}".format(positionRight, positionDown))

    # generate Butttons and attach a function
    b_test = Button(config, text="Print Something",
        command=lambda: bf.callbackTest(),
        height=2, width=15)
    b_start = Button(config, text="Start Thread",
        command= lambda: bf.startThread(args, run_flag, all_processes, b_start),
        height=2, width=15)
    b_end = Button(config, text="Terminate Thread",
        command= lambda: bf.terminateThread(run_flag, b_start),
        height=2, width=15)
    b_map = Button(config, text="Make Map",
        command= lambda: bf.showMap(),
        height=2, width=15)

    # Set position and attach to Tk window
    b_test.place(x = 30, y = 20)
    b_start.place(x = 30, y = 70)
    b_end.place(x = 30, y = 120)
    b_map.place(x = 30, y = 170)

    mainloop()

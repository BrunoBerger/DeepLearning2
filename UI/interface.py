from tkinter import *

from UI import buttonFuncs as bf


def optionWindow(args, run_flag, all_processes):
    # Generate a tkinter window
    config = Tk()
    config.title("Options")
    config.minsize(280,300)
    config.maxsize(350,600)

    # Basically lets the window spawn in the middle of the screen
    # Gets the requested values of the height and widht.
    windowWidth = config.winfo_reqwidth()
    windowHeight = config.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(config.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(config.winfo_screenheight()/2 - windowHeight/2)
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
    b_map = Button(config, text="Show Map",
        command= lambda: bf.showMap(),
        height=2, width=15)

    # Radio Buttons for Type-Selection
    odType = StringVar(config)
    rb_SSD = Radiobutton(config, text="Moblie Net SSD",
        variable=odType, value="MobileNetSSD",
        command= lambda: bf.changeType(args, odType))
    rb_yolo = Radiobutton(config, text="Yolo-Coco",
        variable=odType, value="yolo-coco",
        command= lambda: bf.changeType(args, odType))


    # Set position and attach to Tk window
    b_test.place(x = 30, y = 20)
    b_start.place(x = 30, y = 70)
    b_end.place(x = 30, y = 120)
    b_map.place(x = 30, y = 170)

    rb_SSD.place(x = 160, y = 70)
    rb_yolo.place(x = 160, y = 90)

    rb_SSD.select()
    mainloop()

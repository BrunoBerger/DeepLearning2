from tkinter import *
from geolocation import website

def callbackTest():
    print("Autsch")

def startThread(args, run_flag, all_processes, b_start):
    import main
    run_flag.value = True
    main.initDetectionThread(args, run_flag, all_processes)
    b_start.config(state="disabled")

def terminateThread(run_flag, b_start):
    print("Terminating Stream")
    run_flag.value = False
    b_start.config(state="active")

def showMap():
    website.makeMap()


def optionWindow(args, run_flag, all_processes):
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

    b_test = Button(config, text="Print Something",
        command=lambda: buttonFuncs.callbackTest(),
        height=2, width=15)
    b_start = Button(config, text="Start Thread",
        command= lambda: startThread(args, run_flag, all_processes, b_start),
        height=2, width=15)
    b_end = Button(config, text="Terminate Thread",
        command= lambda: terminateThread(run_flag, b_start),
        height=2, width=15)
    b_map = Button(config, text="Show Map",
        command= lambda: showMap(),
        height=2, width=15)

    b_test.place(x = 30, y = 20)
    b_start.place(x = 30, y = 70)
    b_end.place(x = 30, y = 120)
    b_map.place(x = 30, y = 170)
    mainloop()

# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()

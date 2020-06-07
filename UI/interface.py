from tkinter import *
import multiprocessing

from UI import buttonFuncs as bf

def optionWindow(args, run_flag, all_processes):
    # Generate a tkinter window
    master = Tk()
    master.title("Object Detection")
    master.minsize(275,300)
    master.maxsize(275,300)
    # Gets both half the screen width/height and window width/height
    positionRight = int(master.winfo_screenwidth()/1.5)
    positionDown = int(master.winfo_screenheight()/2.5)
    # Positions the window in the center of the page.
    master.geometry("+{}+{}".format(positionRight, positionDown))

    # checkbox-button for live-toggle render-option
    renderOpt = BooleanVar()
    output_flag = multiprocessing.Value('I', True)
    renderOpt.trace("w", lambda *_: bf.updateRenderMode(output_flag))

    c_render = Checkbutton(master, text="Show Output",
        variable=renderOpt)
    c_render.deselect()

    # generate Butttons and attach a function
    buttonColour="light sky blue"
    b_start = Button(master, text="Start Detecting",
        command= lambda: bf.startThread(args, run_flag, all_processes,
                                        b_start, output_flag),
        height=3, width=15, bg=buttonColour)
    b_stop = Button(master, text="Stop",
        command= lambda: bf.terminateThread(run_flag, b_start),
        height=1, width=5, bg=buttonColour)
    b_map = Button(master, text="Make Map",
        command= lambda: bf.showMap(),
        height=2, width=10, bg=buttonColour)


    # generate explanation Text and Labels
    introText=("This is a tool for detecting objects"
               "\nand logging their GPS-Position."
               "\n\nPlease make sure you have a camera connceted")
    l_intro = Label(master, text=introText, justify=LEFT)

    l_mapInfo = Label(master, justify=LEFT,
                      text="Generates a HTML-file \nand opens it in the browser")

    l_github = Label(master, text="View this project on GitHub", fg="blue")
    l_github.bind("<Button-1>",
        lambda e: bf.openWeblink("https://github.com/BrunoBerger/DeepLearning2"))

    # Visual flair
    v_topLine = Canvas()
    v_topLine.config(width=260, height=2, bg="gray72")
    v_bottomLine = Canvas()
    v_bottomLine.config(width=160, height=2, bg="gray72")

    # Set position and attach to Tk window
    b_start.place(x=30, y=100)
    b_stop.place(x=160, y=100)
    b_map.place(x=15, y=200)

    c_render.place(x=155, y=130)

    l_intro.place(x=10, y=10)
    l_mapInfo.place(x=100, y=201)
    l_github.place(x=58, y=275)

    v_topLine.place(x=5, y=80)
    v_bottomLine.place(x=55, y=175)
    mainloop()

def layoutTest(args, run_flag, all_processes):
    optionWindow(args, run_flag, all_processes)

if __name__ == "__main__":
    args = "test"
    run_flag = "test"
    all_processes = "test"
    layoutTest(args, run_flag, all_processes)

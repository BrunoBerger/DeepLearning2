# Modules needed for the functions
import multiprocessing
import webbrowser

from object_detection import realTimeOnlySSD as od
from geolocation import website

# Starts a detection-thread
def startThread(args, run_flag, all_processes, b_start, output_flag):
    run_flag.value = True
    process = multiprocessing.Process(target=od.main,
                                        args=(args, run_flag, output_flag,))
    process.start()
    all_processes.append(process)

    b_start.config(state="disabled")

def terminateThread(run_flag, b_start):
    print("Terminating Stream")
    run_flag.value = False
    b_start.config(state="active")

def updateRenderMode(output_flag):
    output_flag.value = not output_flag.value

# TODO: Specify behaviour for new tab/window + used Browser
# open a new window/tab
def showMap():
    website.makeMap()

def openWeblink(url):
    webbrowser.open_new(url)

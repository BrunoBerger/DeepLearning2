# Modules needed for the functions
import multiprocessing
from object_detection import realTimeOnlySSD as od
from geolocation import website

# A simple test for buttons
def callbackTest():
    print("Will make a screenshot in the future")

# Starts a detection-thread
def startThread(args, run_flag, all_processes, b_start):
    run_flag.value = True

    process = multiprocessing.Process(target=od.main,
                                        args=(args, run_flag,))
    process.start()
    all_processes.append(process)

    b_start.config(state="disabled")

def terminateThread(run_flag, b_start):
    print("Terminating Stream")
    run_flag.value = False
    b_start.config(state="active")

# open a new window/tab
# TODO: Specify behaviour
def showMap():
    website.makeMap()

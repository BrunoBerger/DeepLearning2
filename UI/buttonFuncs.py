# Modules needed for the functions
import multiprocessing
from object_detection import realTimeCombinedTest as od
from geolocation import website


# A simple test for buttons
def callbackTest():
    print("Autsch")

# get the value of odType and change the model
def changeType(args, odType):
    args["type"] = odType.get()
    print("You chose " + args["type"])

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

import multiprocessing
import time

import realtime_test
import ui_test

def initOD(args):
    realtime_test.initOD(args)

def main():
    run_flag = multiprocessing.Value('I', True)

    # list of all processes, so that they can be killed afterwards
    process = multiprocessing.Process(target=initOD, args=(run_flag,))
    process.start()

    ui_test.optionWindow(run_flag)
    
    process.join()
    print("Process Terminated")

    print("done")

if __name__ == '__main__':
    main()

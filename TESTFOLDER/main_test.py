import multiprocessing
import time

import realtime_test
import ui_test

def initOD(args):
    realtime_test.initOD(args)

def odThread(run_flag, all_processes):
    process = multiprocessing.Process(target=initOD, args=(run_flag,))
    process.start()
    all_processes.append(process)

def main():
    run_flag = multiprocessing.Value('I', True)
    all_processes = []


    ui_test.optionWindow(run_flag, all_processes)

    for process in all_processes:
        process.join()
    print("Process Terminated")

    print("done")

if __name__ == '__main__':
    # list of all processes, so that they can be killed afterwards
    all_processes = []
    main()

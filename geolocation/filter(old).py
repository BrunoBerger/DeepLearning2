from datetime import datetime
import csv

# Reset filterd Objects
f = open("../object_log_filterd.csv", "w+")
f.close()

# Filter similar detections out
with open("../object_log.csv", "r") as objects_raw:
    rawReader = csv.reader(objects_raw, delimiter=',')

    prevRow = next(rawReader)

    # while True:
    #     try:
    #         curRow = next(rawReader)
    #         if prevRow[0] == curRow[0]:
    #             timeDelta = curRow[4] - prevRow[4]
    #             print(timeDelta)
    #         prevRow = curRow
    #     except:
    #         break
    for x in range(0, 30):

        curRow = next(rawReader)
        if prevRow[0] == curRow[0]:
            prevTime = datetime.strptime(prevRow[4], '%Y-%m-%d %H:%M:%S.%f')
            curTime = datetime.strptime(curRow[4], '%Y-%m-%d %H:%M:%S.%f')

            print(curRow[0], curTime)

            detDelta = (curTime - prevTime).total_seconds()
            print(detDelta)
            if detDelta > 2:
                print("LOL GEWINNE GEWINNE GEWINNE GEWINNE!")
        prevRow = curRow

print("[done]")

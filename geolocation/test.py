import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from random import uniform


def givePosition():
    latitude = uniform(50,52)
    longitude = uniform(8,10)
    return latitude, longitude

def idk():
    dataCollums = {'Name':[], 'Lat':[], 'Long':[]}
    data = pd.DataFrame(dataCollums)


    for i in range(10):
        newObject = {'Name': 'Kuh', 'Lat': uniform(50,52), 'Long': uniform(8,10)}
        data = data.append(newObject, ignore_index=True)
    print("Data:")
    print(data)


    BBox = (data.Long.min(), data.Long.max(),
            data.Lat.min(), data.Lat.min())
    print("Bounding Box:", BBox)

def main():
    position = givePosition()
    print(position[1])

if __name__ == '__main__':
	main()

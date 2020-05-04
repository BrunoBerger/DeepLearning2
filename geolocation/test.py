import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from random import uniform


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

img = np.zeros([100,100,3],dtype=np.uint8)
img.fill(255) # or img[:] = 255

fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(data.Long, data.Lat, zorder=1, alpha= 0.2, c='b', s=10)
ax.set_title('Plotting Spatial Data on Riyadh Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(img, zorder=0, extent = BBox, aspect= 'equal')

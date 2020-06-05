import webbrowser
import folium
import csv
import os
from tkinter import filedialog

# Opens a browser-tab with the objects on a map
def makeMap():
    # gets the name of the session-csv the user chooses
    stdFilePath = "logs"
    selectedFile = filedialog.askopenfilename(initialdir = stdFilePath,
                                              title = "Select file",
                                              filetypes = (("Only logs","*.csv"),
                                                           ("all files","*.*")))
    # only do if a file is selected
    if not selectedFile == "":
        # Creates Map Object
        k = folium.Map(location=[52, 9], zoom_start=8)
        # Create Markters of a csv file
        with open(selectedFile, "r") as objects:
            reader = csv.reader(objects, delimiter=',')
            for row in reader:
                lat = row[2]
                lon = row[3]
                name = row[0].capitalize()
                time = row[4]
                popup = "{} found near: {},{}, at {}".format(name,lat,lon,time)
                tooltip = name + " detected"
                folium.Marker([lat, lon],
                    popup=popup,
                    tooltip=tooltip).add_to(k)

        # Save and dislplay the html file
        # (will use the default browser)
        k.save('geolocation/karte.html')
        webbrowser.open('file://' + os.path.realpath("geolocation/karte.html"), new=0)
    else:
        print("[ERROR] Please select a file")

import webbrowser
import folium
import csv


# Creates Map Object
k = folium.Map(location=[52, 9], zoom_start=8)


# Create Markters of a csv file
with open("../object_log.csv", "r") as objects:
    reader = csv.reader(objects, delimiter=',')
    for row in reader:
        lat = row[2]
        lon = row[3]
        obj = row[0]
        popup = "{} found at: {},{}".format(obj,lat,lon)
        folium.Marker([lat, lon],
            popup=popup,
            tooltip=obj).add_to(k)

# Save and dislplay the html file
k.save('karte.html')
webbrowser.open('karte.html', new=0)

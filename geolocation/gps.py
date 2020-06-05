from random import uniform


def givePosition():
    # sim. gps position with ~1m accuracy
    latitude = "%.5f" % uniform(50,52)
    longitude = "%.5f" % uniform(8,10)
    return latitude, longitude

def main():
    position = givePosition()
    print(position[1])

if __name__ == '__main__':
	main()

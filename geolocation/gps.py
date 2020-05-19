from random import uniform


def givePosition():
    latitude = uniform(50,52)
    longitude = uniform(8,10)
    return latitude, longitude

def main():
    position = givePosition()
    print(position[1])

if __name__ == '__main__':
	main()

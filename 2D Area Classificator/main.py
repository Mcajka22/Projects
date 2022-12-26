import math
import time
import random
import matplotlib
matplotlib.use('TkAgg')             # fix for the showcase of the graph
import matplotlib.pyplot as plt

RANGE_X = 5000
RANGE_Y = 5000

TRAIN_PURPLE = [[+4500, +4400], [+4100, +3000], [+1800, +2400], [+2500, +3400], [+2000, +1400]]
TRAIN_BLUE = [[-4500, +4400], [-4100, +3000], [-1800, +2400], [-2500, +3400], [-2000, +1400]]
TRAIN_RED = [[-4500, -4400], [-4100, -3000], [-1800, -2400], [-2500, -3400], [-2000, -1400]]
TRAIN_GREEN = [[+4500, -4400], [+4100, -3000], [+1800, -2400], [+2500, -3400], [+2000, -1400]]

POINTS_LIST = []


def main():

    start = time.time()     # pocitanie casu

    numOfNeighbours = int(input("Enter number of nearest neighbours: "))

    setStartingPoints()

    testing(40000, numOfNeighbours)

    stop = time.time()
    print("Time to complete classification: " + str(stop - start) + " seconds.")

    plotOutput()
    generatedPointsOutput()


def generatedPointsOutput():       # vytvorenie grafu pre generovane body

    for point in POINTS_LIST:
        if point.givenColor == "Purple":
            plt.plot(point.x, point.y, color="purple", marker="o", markersize=3)

        if point.givenColor == "Blue":
            plt.plot(point.x, point.y, color="blue", marker="o", markersize=3)

        if point.givenColor == "Red":
            plt.plot(point.x, point.y, color="red", marker="o", markersize=3)

        if point.givenColor == "Green":
            plt.plot(point.x, point.y, color="green", marker="o", markersize=3)

    plt.grid()
    plt.show()


def plotOutput():         # vytvorenie grafu pre klasifikovanie bodov

    start = time.time()

    for point in POINTS_LIST:
        if point.color == "Purple":
            plt.plot(point.x, point.y, color="purple", marker="o", markersize=5)
        if point.color == "Blue":
            plt.plot(point.x, point.y, color="blue", marker="o", markersize=5)
        if point.color == "Red":
            plt.plot(point.x, point.y, color="red", marker="o", markersize=5)
        if point.color == "Green":
            plt.plot(point.x, point.y, color="green", marker="o", markersize=5)

    stop = time.time()
    print("Time to graph: " + str(stop - start) + " seconds.")

    plt.grid()
    plt.show()


def setStartingPoints():        # nacitanie pociatocnych 20 bodov

    for position in TRAIN_PURPLE:
        temp = POINT(position[0], position[1], "Purple")
        temp.color = "Purple"
        POINTS_LIST.append(temp)

    for position in TRAIN_BLUE:
        temp = POINT(position[0], position[1], "Blue")
        temp.color = "Blue"
        POINTS_LIST.append(temp)

    for position in TRAIN_RED:
        temp = POINT(position[0], position[1], "Red")
        temp.color = "Red"
        POINTS_LIST.append(temp)

    for position in TRAIN_GREEN:
        temp = POINT(position[0], position[1], "Green")
        temp.color = "Green"
        POINTS_LIST.append(temp)


#testing function with the parameter of testing sample size and knn - user entered k nearest neighbours to classify by
def testing(testingSampleSize, knn):
    iterations = testingSampleSize/4    # testing sample size is divided by 4 to get the number of iterations necessary

    incorrectCounter = 0

    # in each iteration 4 points are generated of each color with a 1% chance that a point is going to be generated
    # as an outlier (anywhere on the board), while others are generated close to the given color of region by the training sample
    for i in range(int(iterations)):

        num = random.randint(0, 99)
        temp = POINT(random.randint(-500, 5000), random.randint(-500, 5000), "Purple")
        if num == 0:
            temp = POINT(random.randint(-5000, 5000), random.randint(-5000, 5000), "Purple")
        temp.color = classify(temp.x, temp.y, knn)
        POINTS_LIST.append(temp)
        if temp.color != "Purple":
            incorrectCounter += 1

        #blue
        num = random.randint(0, 99)
        temp = POINT(random.randint(-5000, 500), random.randint(-500, 5000), "Blue")
        if num == 0:
            temp = POINT(random.randint(-5000, 5000), random.randint(-5000, 5000), "Blue")
        temp.color = classify(temp.x, temp.y, knn)
        POINTS_LIST.append(temp)
        if temp.color != "Blue":
            incorrectCounter += 1

        #red
        num = random.randint(0, 99)
        temp = POINT(random.randint(-5000, 500), random.randint(-5000, 500), "Red")
        if num == 0:
            temp = POINT(random.randint(-5000, 5000), random.randint(-5000, 5000), "Red")
        temp.color = classify(temp.x, temp.y, knn)
        POINTS_LIST.append(temp)
        if temp.color != "Red":
            incorrectCounter += 1

        #green
        num = random.randint(0, 99)
        temp = POINT(random.randint(-500, 5000), random.randint(-5000, 500), "Green")
        if num == 0:
            temp = POINT(random.randint(-5000, 5000), random.randint(-5000, 5000), "Green")
        temp.color = classify(temp.x, temp.y, knn)
        POINTS_LIST.append(temp)
        if temp.color != "Green":
            incorrectCounter += 1

    print("Testing sample size: " + str(testingSampleSize))
    print("Incorrectly assigned: " + str(incorrectCounter))


def classify(x, y, k):

    for point in POINTS_LIST:
        getDistance(point, x, y)

    sortedList = sorted(POINTS_LIST, key=lambda d: d.distance, reverse=False)

    KNN_LIST = []

    purpleCounter = 0
    blueCounter = 0
    redCounter = 0
    greenCounter = 0

    i = 0

    while i != k:
        KNN_LIST.append(sortedList[i])
        i += 1

    for point in KNN_LIST:

        match point.color:
            case "Purple":
                purpleCounter += 1
            case "Blue":
                blueCounter += 1
            case "Red":
                redCounter += 1
            case "Green":
                greenCounter += 1

    highestOccur = max(purpleCounter, blueCounter, redCounter, greenCounter)

    if highestOccur == purpleCounter:
        return "Purple"
    elif highestOccur == blueCounter:
        return "Blue"
    elif highestOccur == redCounter:
        return "Red"
    else:
        return "Green"


# calculates the distance of point with target location (target_X/Y) using Pythagoras theorem
def getDistance(point, target_X, target_Y):

    distance = math.sqrt((point.x - target_X)*(point.x - target_X) + (point.y - target_Y)*(point.y - target_Y))
    point.distance = distance


class POINT:

    def __init__(self, x_position, y_position, givenColor):
        self.x = x_position
        self.y = y_position
        self.color = None
        self.givenColor = givenColor
        self.distance = 0


main()

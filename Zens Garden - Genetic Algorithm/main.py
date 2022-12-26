import random
import time
import matplotlib
matplotlib.use('TkAgg')             # fix for the showcase of the graph
import matplotlib.pyplot as plt
from pandas import *


NUM_OF_INDIVIDUALS = 100  # number of individuals in a generation
NUM_OF_GENERATIONS = 100  # number of generations
MUTATION_PROBABILITY = .1  # sets the probability of mutation
SELECTION_METHOD_PERCENTAGE = 15  # sets the percentage of population copied to the next generation and do the crossover

STONE_LOCATIONS = []  # saves location of stones on the board
GARDENER_LIST = []  # current generation of gardeners
OUTER_FIELDS_LIST = []  # saves all the possible positions around the board the gardener can move from
USER_GARDEN = []  # saves the user created garden
NEXT_GENERATION = []  # serves to save the next generation
BEST_OF_EACH_GEN = []  # saves the best performing individual from each generation
BEST_OF_EACH_GEN_FITNESS = []  # saves the fitness of the best performing individual from each generation
AVERAGE_GEN_FITNESS = []  # saves the average fitness for each generation


def main():
    rows = int(input("Enter number of rows: "))
    columns = int(input("Enter number of columns: "))

    add_stones(rows, columns)

    print("\n1.\tElitism Selection")
    print("2.\tRoulette Selection")

    chooseSelectionMethod = int(input("Enter the number corresponding to the desired selection: "))  # user chooses selection method

    start = time.time()
    generatePositions(rows, columns)

    for gen in range(NUM_OF_GENERATIONS):

        if gen == 0:                        # create initial population
            for i in range(NUM_OF_INDIVIDUALS):
                temp = GARDENER(rows, columns)
                GARDENER_LIST.append(temp)

        sumOfFitness = 0

        for gardener in GARDENER_LIST:
            solve(gardener, columns, rows)
            sumOfFitness += gardener.fitness

        sortedByFitness = sorted(GARDENER_LIST, key=lambda x: x.fitness, reverse=True)

        AVERAGE_GEN_FITNESS.append(sumOfFitness / NUM_OF_INDIVIDUALS)

        nextGen15 = []  # list for 15% of individuals selected from a selection method

        if chooseSelectionMethod == 1:
            nextGen15 = elitismSelection(sortedByFitness)
        if chooseSelectionMethod == 2:
            nextGen15 = rouletteSelection(sortedByFitness)

        BEST_OF_EACH_GEN.append(sortedByFitness[0])  # the best individual from each generation gets appended to the given list
        BEST_OF_EACH_GEN_FITNESS.append(sortedByFitness[0].fitness)
        GARDENER_LIST.clear()

        for i in range(NUM_OF_INDIVIDUALS):  # this cycle creates the next generation
            temp = GARDENER(rows, columns)
            GARDENER_LIST.append(temp)

            if i < len(nextGen15):  # 15% of the last generation is put into the population
                GARDENER_LIST[i] = nextGen15[i]
            else:
                GARDENER_LIST[i] = crossover(nextGen15, temp)  # 85% of the next generation is created by crossover

            mutation(GARDENER_LIST[i])

    bestIndividual = BEST_OF_EACH_GEN[0]        # finding the "fittest" gardener
    bestIndividualIndex = 0                     # and his index
    for gardener in BEST_OF_EACH_GEN:
        if gardener.fitness > bestIndividual.fitness:
            bestIndividual = gardener
            bestIndividualIndex = BEST_OF_EACH_GEN.index(bestIndividual)

    stop = time.time()
    timeEfficiency = stop - start

    finalOutput(timeEfficiency, bestIndividual, bestIndividualIndex)


# possible mutation of genes depending on selected mutation probability
def mutation(gardener):
    pathNum = random.randint(1, 10)
    horiNum = random.randint(1, 10)
    vertNum = random.randint(1, 10)
    p = MUTATION_PROBABILITY * 10

    if p >= pathNum:
        num1 = random.randint(0, len(gardener.position_path) - 1)
        num2 = random.randint(0, len(gardener.position_path) - 1)
        gardener.position_path[num1], gardener.position_path[num2] = gardener.position_path[num2], gardener.position_path[num1]

    if p >= vertNum:
        if gardener.turn_vertically == 'r':
            gardener.turn_vertically = 'l'
        elif gardener.turn_vertically == 'l':
            gardener.turn_vertically = 'r'

    if p >= horiNum:
        if gardener.turn_horizontally == 'u':
            gardener.turn_horizontally = 'd'
        elif gardener.turn_horizontally == 'd':
            gardener.turn_horizontally = 'u'


# crossover of the genes of randomly selected parents from the top 15%
def crossover(selected_individuals, temp):
    parent1 = random.choice(selected_individuals)
    parent2 = random.choice(selected_individuals)

    point_of_crossover = random.randint(0, len(parent1.position_path))

    newPath = []

    for i in range(len(parent1.position_path)):
        if i > point_of_crossover:
            newPath.append(parent2.position_path[i])
        else:
            newPath.append(parent1.position_path[i])

    temp.position_path = newPath
    temp.turn_vertically = random.choice([parent1.turn_vertically, parent2.turn_vertically])
    temp.turn_horizontally = random.choice([parent1.turn_horizontally, parent2.turn_horizontally])

    return temp


# the elitism selection selects the best performing 15% of the population
def elitismSelection(sortedArray):
    myList = []
    for i in range(int(NUM_OF_INDIVIDUALS / 100 * SELECTION_METHOD_PERCENTAGE)):
        myList.append(sortedArray[i])

    return myList


# roulette selection, we get the sum of fitness of all individuals and choose a random number between the sum and 0
# after iteratively subtracting the gardeners' fitness, the gardener whose fitness subtracts under 0 is chosen
# 15% of the population is selected

def rouletteSelection(sortedArray):
    myList = []
    sum = 0

    betterHalf = []

    for i in range(int(NUM_OF_INDIVIDUALS/2)):
        betterHalf.append(sortedArray[i])

    for i in range(len(betterHalf)):
        sum += sortedArray[i].fitness

    for i in range(int(NUM_OF_INDIVIDUALS / 100 * SELECTION_METHOD_PERCENTAGE)):

        num = random.randint(0, sum)
        for gardener in sortedArray:

            num -= gardener.fitness
            if num < 0:
                myList.append(gardener)
                break
    return myList


def solve(gardener, columns, rows):  # solves the board for the given gardener depending on his genes (path of starting positions and turns)

    counter = 1
    for position in gardener.position_path:

        gardener.starting_position_x = position[0]
        gardener.starting_position_y = position[1]

        if gardener.starting_position_x == 0:
            if gardener.garden[position[0] + 1][position[1]] != '0':
                continue
            moveDown(gardener, counter)
        elif gardener.starting_position_x == rows + 1:
            if gardener.garden[position[0] - 1][position[1]] != '0':
                continue
            moveUp(gardener, counter)
        elif gardener.starting_position_y == 0:
            if gardener.garden[position[0]][position[1] + 1] != '0':
                continue
            moveRight(gardener, counter)
        elif gardener.starting_position_y == columns + 1:
            if gardener.garden[position[0]][position[1] - 1] != '0':
                continue
            moveLeft(gardener, counter)

        counter += 1

        if gardener.finished_gardening:
            return


# solves downwards movement
def moveDown(gardener, operatorNum):
    new_position_x = gardener.starting_position_x + 1
    new_position_y = gardener.starting_position_y

    if gardener.garden[new_position_x][new_position_y] == 'x':
        return

    if gardener.garden[new_position_x][new_position_y] != '0':
        turnRightLeft(gardener, operatorNum)
        return

    if gardener.garden[new_position_x][new_position_y] == '0':
        gardener.garden[new_position_x][new_position_y] = str(operatorNum)
        gardener.starting_position_x = new_position_x
        gardener.starting_position_y = new_position_y
        gardener.fitness += 1
        if gardener.fitness == gardener.target_fitness:
            gardener.finished_gardening = True
            gardener.solved = True
        moveDown(gardener, operatorNum)


# solves upwards movement
def moveUp(gardener, operatorNum):
    new_position_x = gardener.starting_position_x - 1
    new_position_y = gardener.starting_position_y

    if gardener.garden[new_position_x][new_position_y] == 'x':
        return

    if gardener.garden[new_position_x][new_position_y] != '0':
        turnRightLeft(gardener, operatorNum)
        return

    if gardener.garden[new_position_x][new_position_y] == '0':
        gardener.garden[new_position_x][new_position_y] = str(operatorNum)
        gardener.starting_position_x = new_position_x
        gardener.starting_position_y = new_position_y
        gardener.fitness += 1
        if gardener.fitness == gardener.target_fitness:
            gardener.finished_gardening = True
            gardener.solved = True
        moveUp(gardener, operatorNum)


# solves rightwards movement
def moveRight(gardener, operatorNum):
    new_position_x = gardener.starting_position_x
    new_position_y = gardener.starting_position_y + 1

    if gardener.garden[new_position_x][new_position_y] == 'x':
        return

    if gardener.garden[new_position_x][new_position_y] != '0':
        turnUpDown(gardener, operatorNum)
        return

    if gardener.garden[new_position_x][new_position_y] == '0':
        gardener.garden[new_position_x][new_position_y] = str(operatorNum)
        gardener.starting_position_x = new_position_x
        gardener.starting_position_y = new_position_y
        gardener.fitness += 1
        if gardener.fitness == gardener.target_fitness:
            gardener.finished_gardening = True
            gardener.solved = True
        moveRight(gardener, operatorNum)


# solves leftwards movement
def moveLeft(gardener, operatorNum):
    new_position_x = gardener.starting_position_x
    new_position_y = gardener.starting_position_y - 1

    if gardener.garden[new_position_x][new_position_y] == 'x':
        return

    if gardener.garden[new_position_x][new_position_y] != '0':
        turnUpDown(gardener, operatorNum)
        return

    if gardener.garden[new_position_x][new_position_y] == '0':
        gardener.garden[new_position_x][new_position_y] = str(operatorNum)
        gardener.starting_position_x = new_position_x
        gardener.starting_position_y = new_position_y
        gardener.fitness += 1
        if gardener.fitness == gardener.target_fitness:
            gardener.finished_gardening = True
            gardener.solved = True
        moveLeft(gardener, operatorNum)


# solves vertical movement turning
def turnRightLeft(gardener, operatorNum):
    if gardener.turn_vertically == 'r':
        if gardener.garden[gardener.starting_position_x][gardener.starting_position_y + 1] == 'x' or \
                gardener.garden[gardener.starting_position_x][gardener.starting_position_y + 1] == '0':
            moveRight(gardener, operatorNum)
        else:
            if gardener.garden[gardener.starting_position_x][gardener.starting_position_y - 1] == 'x' or \
                    gardener.garden[gardener.starting_position_x][gardener.starting_position_y - 1] == '0':
                moveLeft(gardener, operatorNum)
            else:
                gardener.finished_gardening = True
                return

    elif gardener.turn_vertically == 'l':
        if gardener.garden[gardener.starting_position_x][gardener.starting_position_y - 1] == 'x' or \
                gardener.garden[gardener.starting_position_x][gardener.starting_position_y - 1] == '0':
            moveLeft(gardener, operatorNum)
        else:
            if gardener.garden[gardener.starting_position_x][gardener.starting_position_y + 1] == 'x' or \
                    gardener.garden[gardener.starting_position_x][gardener.starting_position_y + 1] == '0':
                moveRight(gardener, operatorNum)
            else:
                gardener.finished_gardening = True
                return


# solves horizontal movement turning
def turnUpDown(gardener, operatorNum):
    if gardener.turn_horizontally == 'u':
        if gardener.garden[gardener.starting_position_x - 1][gardener.starting_position_y] == 'x' or \
                gardener.garden[gardener.starting_position_x - 1][gardener.starting_position_y] == '0':
            moveUp(gardener, operatorNum)
        else:
            if gardener.garden[gardener.starting_position_x + 1][gardener.starting_position_y] == 'x' or \
                    gardener.garden[gardener.starting_position_x + 1][gardener.starting_position_y] == '0':
                moveDown(gardener, operatorNum)
            else:
                gardener.finished_gardening = True
                return

    elif gardener.turn_horizontally == 'd':
        if gardener.garden[gardener.starting_position_x + 1][gardener.starting_position_y] == 'x' or \
                gardener.garden[gardener.starting_position_x + 1][gardener.starting_position_y] == '0':
            moveDown(gardener, operatorNum)
        else:
            if gardener.garden[gardener.starting_position_x - 1][gardener.starting_position_y] == 'x' or \
                    gardener.garden[gardener.starting_position_x - 1][gardener.starting_position_y] == '0':
                moveUp(gardener, operatorNum)
            else:
                gardener.finished_gardening = True
                return


# adds stones on user selected positions
def add_stones(rows, columns):
    i = 0

    while 1:

        add = input("Add stone (y/n): ")
        if add == 'n':
            break

        if add == 'y':
            x = int(input("Enter stone no. " + str(i + 1) + "x coordinate: "))
            y = int(input("Enter stone no. " + str(i + 1) + "y coordinate: "))
            stone_coord = (x, y)
            if x < 0 or x > rows or y < 0 or y > columns:
                print("Position out of bounds.")
                continue
            else:
                i += 1
                STONE_LOCATIONS.append(stone_coord)

        else:
            continue


# creates garden from user inputs
def init_garden(rows, columns):
    board = [['0' for x in range(columns + 2)] for y in range(rows + 2)]

    i = 0

    while i < rows + 2:
        j = 0
        while j < columns + 2:
            if i == 0 or j == 0:
                board[i][j] = 'x'
            if i == rows + 1 or j == columns + 1:
                board[i][j] = 'x'

            board_cord = (i, j)
            if board_cord in STONE_LOCATIONS:
                board[i][j] = 's'
            j += 1
        i += 1

    return board


# generates starting positions list
def generatePositions(rows, columns):
    i = 0
    fieldCounter = 0
    while i < rows + 2:
        j = 0
        while j < columns + 2:
            position = (i, j)
            if i == 0 or i == rows + 1:
                if j == 0 or j == columns + 1:
                    pass
                else:
                    OUTER_FIELDS_LIST.append(position)
                    fieldCounter += 1
            if j == 0 or j == columns + 1:
                if i == 0 or i == columns + 1:
                    pass
                else:
                    OUTER_FIELDS_LIST.append(position)
                    fieldCounter += 1
            j += 1
        i += 1


# generates gardeners path
def getRandomPath(rows, columns):
    myList = []

    """ firstList = []
    secondList = []

    for position in OUTER_FIELDS_LIST:              #idea to pair the values to "optimize?" the path of starting positions
        if position[0] == 0:
            firstList.append(position)
        elif position[0] == rows+1:
            secondList.append(position)

    for position in OUTER_FIELDS_LIST:
        if position[1] == 0:
            firstList.append(position)
        elif position[1] == columns+1:
            secondList.append(position) """

    counter = 0

    while counter != rows + columns + len(STONE_LOCATIONS) - 2:  # the sequence of outer fields is the size of rows+columns+numberOfStones -2
        chosenPosition = random.choice(OUTER_FIELDS_LIST)
        if chosenPosition in myList:
            continue
        else:
            myList.append(chosenPosition)
            counter += 1

    return myList


def finalOutput(timeEfficiency, bestIndividual, bestIndividualIndex):
    print("Best individual garden: ")

    #for line in bestIndividual.garden:         #klasicky print do konzole
    #   print(line)

    print(DataFrame(bestIndividual.garden))     # data frame z pandas kniznice
    print("Individuals' starting position path:")
    print(bestIndividual.position_path)
    print("Best individual generation: " + str(bestIndividualIndex))
    print("Best individual fitness: " + str(bestIndividual.fitness))
    print("Vertical turn preference: " + str(bestIndividual.turn_vertically))
    print("Horizontal turn preference: " + str(bestIndividual.turn_horizontally))
    print("Time to complete algorithm: " + "{:.2f}".format(timeEfficiency) + " seconds.")

    generations = range(0, NUM_OF_GENERATIONS)                          # graph
    plt.plot(generations, BEST_OF_EACH_GEN_FITNESS, label="Best")
    plt.plot(generations, AVERAGE_GEN_FITNESS, label="Average")
    plt.legend()
    plt.title("Best and average fitness of generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.show()


# gardener class, at first generation the attributes are assigned randomly
class GARDENER:
    def __init__(self, rows, columns) -> None:
        self.starting_position_x = 0  # these positions showcase the current position of the gardener throughout the movement algorithm
        self.starting_position_y = 0

        self.turn_vertically = random.choice(['r', 'l'])
        self.turn_horizontally = random.choice(['u', 'd'])
        self.garden = init_garden(rows, columns)
        self.position_path = getRandomPath(rows, columns)
        self.fitness = 0
        self.target_fitness = rows * columns - len(STONE_LOCATIONS)
        self.finished_gardening = False
        self.solved = False


main()

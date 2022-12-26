import time

OPERATORS = [(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]    #operatory - mnozina legalnych tahov jazdca na sachovnici 
SIZE = 0                                                          
BOARD = []                            
NUM_OF_MOVES = 0                     #pocitadlo pre prehladane stavy
MAX_NUM_OF_MOVES = 1500000           #maximalny mozny pocet prehladanych stavov pre algoritmus kvoli efektivnosti


def main():
    global SIZE,BOARD,start
    print()
    SIZE = int(input("Enter size of board: "))
    
    x = int(input("Enter x coordinate of the starting position: "))
    y = int(input("Enter y coordinate of the starting position: "))
    
    start = time.time()                                  #spustenie casovaca

    if 0>x or x>SIZE-1 or 0>y or y>SIZE-1:               #kontrola správnosti vstupu pre štartovnú pozíciu
        print("The entered starting position is out of bounds for the chessboard of given size! Restart the program!")
        return
    
    startingPosition = (x,y)
    BOARD = SimBoard(startingPosition)              #inicializacia plochy
    startKnightsTour(startingPosition)              #startovacia funkcia

def startKnightsTour(startingPosition):         #startovacia funkcia na spustenie prehladavania stavov a finalny vypis podla dosiahnutia cieloveho stavu
    print()
    print("Starting Knight's Tour at position: ("+str(startingPosition[0])+","+str(startingPosition[1])+")")
    moveKnight()                    #rekurzivna funkcia prhladavania do hlbky 

    if BOARD.efficiencyLimit == True:               #dosiahnuty maximalny limit prehladaných uzlov 
        print("The algorithm was killed because the maximum number of moves has been reached.") 
    
    elif BOARD.success == False:                #kontrola ci sa nasiel cielovy stav - ak nie z danej pozicie nie je mozne vykonať eulerov tah
        print("The Knight's Tour cannot be executed from the given starting position.")
    
    else:                   #BOARD.success == True - uspesne najdeny cielovy stav, zobrazenie sachovnice a vypis cesty
        printBoard()
        print()
        print("*****-Final Path-*****")
        print(BOARD.path)
    
    stop = time.time()      #zastavenie merania trvania algoritmu
    
    print()
    print("*****-Results-*****")
    print("Number of executed moves: "+ str(NUM_OF_MOVES))
    print("Time to complete algorithm: "+"{:.2f}".format(stop-start)+" seconds.")

#vráti list s možnými tahmi z daneho stavu, ktore aj reprezentuju detske nody pre dany stav
def currentLegalMoves(position):
    global BOARD
    nextPossiblePositions = []
    
    for move in OPERATORS:
        nextPosition = (position[0]+move[0],position[1]+move[1])

        if 0 <= nextPosition[0] < SIZE and 0 <= nextPosition[1] < SIZE:
            if nextPosition not in BOARD.markedFields:
                nextPossiblePositions.append(nextPosition)
    
    return nextPossiblePositions

#trieda reprezentujuca sachovnicu/stav, obsahuje attributy ako cestu (v poradi prejdene polia), oznacene polia (uz prejdene polia),
# sucasnu poziciu (pole na ktorom sa momentalne nachadza), hlbku (v akom tahu sa nachadzame), a bool success/bool efficiencyLimit urcujú
# ci je dosiahnuty cielovy stav/max. pocet krokov

class SimBoard: 

    def __init__(self,startingPosition):
        self.markedFields = []                         
        self.path = []
        self.position = startingPosition                
        self.depth = 0
        self.success = False                        
        self.efficiencyLimit = False
    
    def isMarked(self,move):
        if move in self.markedFields:
            return True
        return False

    def addToPath(self):        #prida danu poziciu do zoznamu prejdených poli, inkrementuje hlbku a prida poziciu do oznacenych poli, inkrementuje počet prehladaných uzlov
        global NUM_OF_MOVES
        self.path.append(self.position)
        self.depth += 1
        self.markedFields.append(self.position)
        NUM_OF_MOVES += 1

    def removeFromPath(self):    #odstrani danu poziciu zo zoznamu prejdených poli a oznacenych poli a inkrementuje hlbku
        self.path.pop()
        self.depth -= 1
        self.markedFields.pop()


def printBoard():    #funkcia sluzi na vytvorenie n*n pola, ocislovanie poli ako konkretne tahy pre eulerov tah a zobrazenie pola
    tempBoard = [[0 for x in range(SIZE)] for y in range(SIZE)] 
    
    index = 1

    for pos in BOARD.path:
        tempBoard[pos[1]][pos[0]] = index
        index += 1
        
    print()

    print("*****-The Final Board-*****")
    for i in tempBoard:
        print(i)
    
def moveKnight():                                    #funckia reprezentujuca tah jazdca - rekurzivne prehladavanie sachovnice
    ##print("Current position: "+str(BOARD.position))             
    BOARD.addToPath()                               #sucasna pozicia sa prida do cesty a oznacenych poli
    ##print("Current Path: "+str(BOARD.path))
    ##print("Depth: "+ str(BOARD.depth))
    
    if NUM_OF_MOVES == MAX_NUM_OF_MOVES:              #kontrolna podmienka dosiahnutia zvoleneho maximalneho poctu prehladaných uzlov
            BOARD.efficiencyLimit = True
            return


    if BOARD.depth == SIZE**2:                           #podmienka ci hlbka je rovna velkosti pola x*x, ak ano nasli sme cielovy stav
        print("The knight's tour is complete!")      
        BOARD.success = True                            #nastavenie cieloveho stavu
        return
    moves = currentLegalMoves(BOARD.position)           #zoznam legalnych tahov zo sucasnej pozicie (deti daneho stavu)(legalne tahy su tahy ktore nie su mimo sachovnice a nie su uz oznacene) 
   
    for move in moves:                                  #iterovanie mnozinou legalnych tahov

        if BOARD.success or BOARD.efficiencyLimit:      #podmienka dosiahnutia cieloveho stavu, v pripade najdenia cieloveho stavu tu vyhasina rekurzia
            break
        ##print("Trying move: "+str(move))
        
        BOARD.position = move                           #aktualizuje sa sucasny pozicia na novy tah ktory presiel kontrolnými podmienkami
                
        moveKnight()                                    #rekurzivne volanie funkcie 
        
    if (BOARD.success == False):                        #kontrolna podmienka ak uz z danej pozicie nie je mozny tah (presli sme vsetky tahy a nesli sme do rekurzie kvoli ilegalite tahov) odstranujeme posledny tah
        ##print("Removing from path")
        BOARD.removeFromPath()                 
                                     
main()
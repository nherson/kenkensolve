from time import time
import kenken
import os
import sys

stdout = sys.stdout
devnull = open(os.devnull, 'w')

def beginFullBenchmark():
    """
    Solves a series of KenKen puzzles, and times them, giving the times
    as puzzles are solved.
    """
    #makes it so nothing gets printed from the normal operation of the program
    #redirects all prints to /dev/null, meaning they just go to nothing 
    #we will change this back once we want to report the timings
    
    puzzleDir = "puzzles/"

    #FOLLOW THIS FORMAT FOR ADDING TESTS TO THIS BENCHMARKING FILE
    currentPuzzle = "nyt6x6_05-01.kk"
    printing(False)
    startTime = time()
    kenken.main(puzzleDir + currentPuzzle)
    stopTime = time()
    printing(True)
    print(currentPuzzle + " solved in " + str(stopTime - startTime) + " seconds")
    
def printing(b):
    if b:
        sys.stdout = stdout
    else:
        sys.stdout = devnull
        

    
if __name__ == "__main__":
    beginFullBenchmark()

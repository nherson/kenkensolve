from time import time
import kenken
import os
import sys


#Globals for StandardOutput and DevNull files for writing to
#These toggle print statements essentially
stdout = sys.stdout
devnull = open(os.devnull, 'w')
puzzleDir = "puzzles/"

def beginFullBenchmark():
    """
    Solves a series of KenKen puzzles, and times them, giving the times
    as puzzles are solved.
    """
    
    #FOLLOW THIS FORMAT FOR ADDING TESTS TO THIS BENCHMARKING FILE
    currentPuzzle = "nyt6x6_05-01.kk"
    printing(False)
    startTime = time()
    kenken.main(puzzleDir + currentPuzzle)
    stopTime = time()
    printing(True)
    print(currentPuzzle + " solved in " + str(stopTime - startTime) + " seconds")

def beginSingleBenchmark(filename):
    printing(False)
    startTime = time()
    kenken.main(puzzleDir + filename)
    stopTime = time()
    printing(True)
    print(filename + " solved in " + str(stopTime - startTime) + " seconds")

 
    
def printing(b):
    """
    If True, enables printing
    If False, disables printing (printing gets sent to nothingness... the great null)
    """
    if b:
        sys.stdout = stdout
    else:
        sys.stdout = devnull
        

    
if __name__ == "__main__":
    try:
        if (sys.argv[1]):
            beginSingleBenchmark(sys.argv[1])
            exit()
    except IndexError:
        pass
    beginFullBenchmark()

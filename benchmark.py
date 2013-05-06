from time import time
import kenken
import os
import sys


#Globals for StandardOutput and DevNull files for writing to
#These toggle print statements essentially
stdout = sys.stdout
devnull = open(os.devnull, 'w')
puzzleDir = "puzzles/"
implementedSolvingMethods = ["arcCon", "arcConLCV", "backTrack"] 

fullBenchmarkPuzzles = ["nyt4x4.kk", "nyt6x6_04-26.kk", "nyt6x6_04-27.kk", "nyt6x6_05-01.kk", 
                        "medium6x6.kk", "hard8x8.kk"] 

def beginFullBenchmark():
    """
    Solves a series of KenKen puzzles, and times them, giving the times
    as puzzles are solved.
    """
    
    #FOLLOW THIS FORMAT FOR ADDING TESTS TO THIS BENCHMARKING FILE
    print("puzzles take longer and longer to solve, Ctrl-C may be necessary in time")
    for puzzle in fullBenchmarkPuzzles:
        for method in implementedSolvingMethods:
            currentPuzzle = "nyt6x6_05-01.kk"
            printing(False)
            startTime = time()
            kenken.main(puzzleDir + currentPuzzle, method)
            stopTime = time()
            printing(True)
            print(currentPuzzle + " solved in " + str(stopTime - startTime) + " seconds using " + method)
        

    

def beginSingleBenchmark(filename):
    for method in implementedSolvingMethods:
        printing(False)
        startTime = time()
        kenken.main(puzzleDir + filename, method)
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

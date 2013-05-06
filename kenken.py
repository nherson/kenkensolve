#############################################################
# A basic KenKen Puzzle solver (v1.0)                       #
# Used Constraint Satisfaction Problem properties           #
# using N-ary constraints to solve KenKen puzzles           #
#                                                           #
# Great for checking answers, or maybe just for after       #
# you've given up :)                                        #
#                                                           #
#                                                           #
# Author: Nicholas Herson (nicholas.herson@berkeley.edu)    #
#                                                           #
#############################################################

import sys
import coordinate
import constraint
import os
from arcConsistency import arcConsistency
from backtrack import BackTrack

def parseConstraint(line):
    """
    Take in a string from a KenKen layout file and generate a tuple containing:
    - The function for the constraint equation (add, mul, sub, con)
    - An integer representing the value the function should evaluate to
    - A list of (x,y) locations involved with the constraint

    Error checks as it goes, making sure each constraint has the appropriate number of involved coordinates
    """
    tokens = line.split()
    if (tokens[0] == "add"):
        if (len(tokens[2:]) < 2):
            raise ValueError("line: " + line + "...Error: incorrect number of coordinates")
        func = kkAdd
    elif (tokens[0] == "sub"):
        if (len(tokens[2:]) != 2):
            raise ValueError("line: " + line + "...Error: incorrect number of coordinates")
        func = kkSub
    elif (tokens[0] == "mul"):
        if (len(tokens[2:]) < 2):
            raise ValueError("line: " + line + "...Error: incorrect number of coordinates")
        func = kkMul
    elif (tokens[0] == "div"):
        if (len(tokens[2:]) != 2):
            raise ValueError("line: " + line + "...Error: incorrect number of coordiantes")
        func = kkDiv
    elif (tokens[0] == "con"):
        if (len(tokens[2:]) != 1):
            raise ValueError("line: " + line + "...Error: incorrect number of coordinates")
        func = kkCon
    else:
        raise NameError("Could not parse function in constraint: " + tokens[0])
    
    #Make sure that the proposed result checks out
    try:
        if (int(tokens[1])%1 != 0.0):
            raise NameError("line: " + line + "...Error: evaluation result must be a whole number")
        else:
            result = int(tokens[1])
    except ValueError:
        raise ValueError("line: " + line + "...Error: " + tokens[1] + " is not a number")

    #Strip the coordinate strings down and make them (x,y) tuples
    coords = []
    for coord in tokens[2:]:
        coord = coord[1:-1]
        coord = coord.split(",")
        try:
            coord = (int(coord[0]), int(coord[1]))
        except ValueError:
            raise ValueError("line: " + line + "...Error: " + str(coord) + " does not appear to be a valid coordinate")
        coords.append(coord)

    return (func, result, coords)


####### KENKEN EVALUATION FUNCTIONS #############
# All functions attempt to calculate the result #
# If there are any coordinate values given      #
# which are not yet assigned (i.e they          #
# are still set to None) which are passed into  #
# the function, None will be returned           #
#################################################

def kkAdd(*args):
    """
    KenKen function of adding coordinates
    It just adds everything in args
    """
    if (None in args):
        return None
    total = 0
    for arg in args:
        total += arg
    return total

def kkSub(*args):
    """
    KenKen version of subtraction
    Can't have negative values, so this takes the absolute value of the difference
    """
    if (None in args):
        return None
    return abs(args[0]-args[1])

def kkMul(*args):
    """
    KenKen version of multiplication
    Simply takes the product of all args
    """
    if (None in args):
        return None
    product = 1
    for arg in args:
        product *= arg
    return product

def kkDiv(*args):
    """
    KenKen version of division
    Makes sure that the numbers are divided in a way such that
    the result is greater than 1.
    """
    if (None in args):
        return None
    quot = float(args[0]) / float(args[1])
    if (quot > 1):
        return quot
    else:
        return 1/quot

def kkCon(*args):
    """
    KenKen constant evaluator
    This just returns what's in the box
    """ 
    if (None in args):
        return None
    return args[0]

class Board:
    """
    Class for the Board object
    The Board serves as a massive container that holds all of the coordinates,
    constraints, and basically all the information about the state of the game.
    When instantiated, the Board generates all of the Coordinates it needs.
    The Board does NOT generate the constraints for you, and must be supplied
    through the 'addConstraint' method.
    
    Once constraints are added, the board is a good container for all game state information.
    Constraints can be retrieved using getConstraint/getConstraints and the constraints then
    have their own isBroken method, which only relies on its own data to check
    """
    def __init__(self, size):
        self.size = size
        startDomain = [i+1 for i in range(size)]
        self.coordinates = []
        for i in range(size):
            for j in range(size):
                self.coordinates.append(coordinate.Coordinate(i, j, startDomain))
        self.constraints = []
        self.fullDomain = [x+1 for x in range(self.size)]

    def getColumn(self, colNum):
        #Return a list of coordinates making up a column
        return self.coordinates[colNum*self.size:(colNum+1)*self.size]

    def getRow(self, rowNum):
        #Return a list of coordinates making up a row
        row = []
        i = rowNum
        while (i < self.size*self.size):
            row.append(self.coordinates[i])
            i += self.size
        return row

    def addConstraint(self, constraint):
        self.constraints.append(constraint)
        
    def getConstraints(self):
        return self.constraints

    def getCoordinates(self):
        return self.coordinates

    def getCoordinate(self, x, y):
        return self.coordinates[self.size*x + y]

    def getSize(self):
        return self.size

def generateRCConstraints(board):
    """
    Generate all constraints on board, using its size as an indicator
    """
    constraints = []
    for i in range(board.getSize()):
        constraints.append(constraint.RCConstraint(board, board.getRow(i)))
        constraints.append(constraint.RCConstraint(board, board.getColumn(i)))
    return constraints

def generateArithmeticConstraint(board, simpleConstraint):
    """
    Generates an ArithmeticConstraint object from the 
    simple tuplified constraints created in parseConstraint(line)
    funtion call, located elsewhere in this file
    """
    func = simpleConstraint[0]
    result = simpleConstraint[1]
    coordinates = []
    for x,y in simpleConstraint[2]:
        coordinates.append(board.getCoordinate(x, y))
    return constraint.ArithmeticConstraint(func, result, coordinates)
    


def main(kenkenFileName, method):
    """
    Make sure supplied info is correct for solving a KenKen file
    """
    try:
        kkFile = open(kenkenFileName)
    except IOError:
        raise IOError("Error: could not find KenKen file '" + sys.argv[1] + "'")
    
    #Get a list of non-trivial lines from the KenKen config file
    kenkenLines = [line.strip() for line in kkFile.readlines() if line is not '']
    
    #The first line should be the size of the board.
    try:
        if (float(kenkenLines[0]) % 1 != 0):
            raise NameError("line: " + kenkenLines[0] + "...Error: board size must be an integer")
        boardSize = int(kenkenLines[0])
    except ValueError:
        raise ValueError("line: " + kenkenLines[0] + "...Error: first line must be a single int for size")

    #Initialize the board
    #This will go ahead and also create the Coordinate objects and place them inside the board
    kenkenBoard = Board(boardSize)
    
    #Generate the RCConstraints (RC = Row and Column)
    for rowColumnConstraint in generateRCConstraints(kenkenBoard):
        kenkenBoard.addConstraint(rowColumnConstraint)
        for coord in rowColumnConstraint.getCoordinates():
            coord.addConstraint(rowColumnConstraint)
    
    #Parse the ArithmeticConstraints and add them to the board
    #See puzzles/puzzle_example.kk for how KenKen layout files should look
    for line in kenkenLines[1:]:
        simplifiedConstraint = parseConstraint(line)
        arithmeticConstraint = generateArithmeticConstraint(kenkenBoard, simplifiedConstraint)
        kenkenBoard.addConstraint(arithmeticConstraint)
        for coord in arithmeticConstraint.getCoordinates():
            coord.addConstraint(arithmeticConstraint)
    
    #######
    # At this point in the main sequence, the kenkenBoard is entirely configured
    # The Coordinates have been established, and both the Row/Column and Arithmetic
    # constraints have been created and added to the kenkenBoard
    # Now it's time to solve the damn thing.
    # 
    # For now, only a naive arcConsistency method is implemented.
    # Future revisions can add some command line arg checking to determine which
    # method to use to solve the board.
    #######

    solver = arcConsistency(kenkenBoard)

    if (method == None or method == "arcCon"):
        solver = arcConsistency(kenkenBoard)
        solveIt = solver.solve
    elif (method == "arcConLCV"):
        solver = arcConsistency(kenkenBoard)
        solveIt = solver.solveWithLCV
    elif (method == "backTrack"):
        solver = BackTrack(kenkenBoard)
        solveIt = solver.solve
    else:
        raise NameError("undefined solving method" + str(method))

    solved = solveIt()
    if (solved == True):
        print("Solution Found:")
        for i in range(kenkenBoard.getSize()):
            print("Column " + str(i))
            print("##########")
            for j in range(kenkenBoard.getSize()):
                print("(" + str(kenkenBoard.getCoordinate(i, j).getX()) + "," +
                    str(kenkenBoard.getCoordinate(i,j).getY()) + "): " +
                     str(kenkenBoard.getCoordinate(i,j).getValue()))
            print("")
    else:
        print("No solution was found. Perhaps the KenKen file is misconfigured?")


#Get the ball rolling with the main() function
if __name__ == "__main__":
    if (len(sys.argv) == 2):
        main(sys.argv[1], None)
    if (len(sys.argv) == 4 and sys.argv[2] == "-m"):
        main(sys.argv[1], sys.argv[3])




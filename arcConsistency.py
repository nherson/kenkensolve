import itertools
import coordinate

def arcConsistencyBacktracking(board):
    """
    Takes in a board, and runs the arcConsistency technique to find a solution to the KenKen,
    if one exists.
    Steps:
    1. Throw every (Coordinate, Constraint) pair onto the consistencyQueue and check consistency
        for all values in the coordinate's domain
            - Eliminate values as necessary
    2. If a variable is pruned, take all Coordinates linked to the current Coordinate via a constraint,
        and put them into the queue (if they aren't already
    3. When the queue is empty:
        - Make sure all Coordinates still have domains of size >= 1
            - If not, backtrack (by throwing a NoSolution exception)
        - If all domains are size 1, we have a solution --> YAY!
        - If some domains are bigger than 1:
            - Find the smallest domain of size 2 or greater, and assign a value
                - Recurse and continue arcConsistency
    Returns True IFF a solution is found
        board will be modified, and the calling function [main()] will be able to analyze the 
        contents of the board to find the solution that was found
    """
    #Just get a local copy of the coordinates, for convenience
    coordinates = []
    for i in range(board.getSize()):
        for coord in board.getRow(i):
            coordinates.append(coord)

    #Initialize the Queue
    consistencyQueue = []

    #Add all (Coordiante, Constraint) pairs to the queue to start
    for coord in coordinates:
            for constraint in coord.getConstraints():
                if (coord, constraint) not in consistencyQueue:
                    consistencyQueue.append((coord, constraint))
 
    def arcConsistencyHelper(board):
        """
        The helper function is recurses every time the queue is emptied,
        and a coordinate must be assigned a value.  When the helper function
        finds a solution, it throws a "Solution" exception, which immediately exits all
        recursion and is caught outside the helper function (neat!).
        """
        while (len(consistencyQueue) != 0):
            #Keep looping until all constraints are satisfied, and no more pruning is available
            currentCoordinate, currentConstraint = consistencyQueue.pop(0)
            relatedCoordinates = [coord for coord in currentConstraint.getCoordinates() if coord != currentCoordinate]
            for value in currentCoordinate.getDomain():
                #Find a set of Coordinate assignments that satisfies the Constraint for this value
                for instance in itertools.product(*[coord.getDomain() for coord in relatedCoordinates]):
                    if currentConstraint.valuesSatisfyConstraint((value,) + instance):
                        break
                #Nothing satisfies? Then prune the value from the domain, and add associated
                #(Coordinate, Constraint) pairs onto the queue
                else:
                    currentCoordinate.removeFromDomain(value)
                    addRelatedToQueue(currentCoordinate)
    
        #Is there an empty domain?
        for coord in coordinates:
            if (len(coord.getDomain()) == 0):
                raise NoSolution("no solution found")

        #Have we found a solution?
        for coord in coordinates:
            if (len(coord.getDomain()) != 1):
                break
        else:
            raise Solution()        

        #None of the above? lets assign a variable and recurse.
        #But first, let's save our current state, so we can 
        #backtrack to it if needed.
        savedDomains = [] #same order as "coordinates" variable
        for coord in coordinates:
            savedDomains.append(coordinate.deepcopy(coord.getDomain()))
        smallestDomainIndex = None
        for i in range(len(savedDomains)):
            if ((smallestDomainIndex == None or len(savedDomains[i]) < len(savedDomains[smallestDomainIndex]))
                                            and (len(savedDomains[i]) > 1)):
                smallestDomainIndex = i
        for x in savedDomains[smallestDomainIndex]:
            coordinates[smallestDomainIndex].setDomain([x,])
            try:
                addRelatedToQueue(coordinates[smallestDomainIndex])
                arcConsistencyHelper(board)
            except NoSolution:
                for i in range(len(savedDomains)):              #Restore the domains if the assignment fails
                    coordinates[i].setDomain(savedDomains[i])

        #Getting to this point means every value in a coordinate's domain has been assigned
        #and nothing allows for satisfaction of constraints down the road.  This means we are left
        #with no other options; there is no solution.
        raise NoSolution()

    def addRelatedToQueue(coordinate):
        for constraint in coordinate.getConstraints():
            for coord in constraint.getCoordinates():
                if (coord, constraint) not in consistencyQueue:
                    consistencyQueue.append((coord, constraint))

  
    #Attempt the helper method, and if a Solution is found, it'll be caught.        
    try:
        arcConsistencyHelper(board)
    except Solution:
        return True
    #In the event that no solution exists
    except NoSolution:
        return False

#Extensions of generic exceptions, used to take advantage
#of exception throwing to navigate around the code efficiently
class Solution(Exception):
    def dummy():
        return #does nothing

class NoSolution(Exception):
    def dummy():
        return #does nothing

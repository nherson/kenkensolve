import itertools
import coordinate

def arcConsistency(board):
    coordinates = []
    for i in range(board.getSize()):
        for coord in board.getRow(i):
            coordinates.append(coord)
    def arcConsistencyHelper(board):
        consistencyQueue = []
        for coord in coordinates:
            for constraint in coord.getConstraints():
                if (coord, constraint) not in consistencyQueue:
                    consistencyQueue.append((coord, constraint))
        while (len(consistencyQueue) != 0):
            #Keep looping until all constraints are satisfied, and no more pruning is available
            currentCoordinate, currentConstraint = consistencyQueue.pop(0)
            relatedCoordinates = [coord for coord in currentConstraint.getCoordinates() if coord != currentCoordinate]
            for value in currentCoordinate.getDomain():
                for instance in itertools.product(*[coord.getDomain() for coord in relatedCoordinates]):
                    if currentConstraint.valuesSatisfyConstraint((value,) + instance):
                        break
                else:
                    currentCoordinate.removeFromDomain(value)
                    for const in currentCoordinate.getConstraints():
                        for coord in const.getCoordinates():
                            if (coord, const) not in consistencyQueue:
                                consistencyQueue.append((coord, const))

        #is there an empty domain?
        for coord in coordinates:
            if (len(coord.getDomain()) == 0):
                raise NoSolution("no solution found")

        #have we found a solution?
        for coord in coordinates:
            if (len(coord.getDomain()) != 1):
                break
        else:
            raise Solution()        

        #none of the above? lets assign a variable and recurse
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
                arcConsistencyHelper(board)
            except NoSolution:
                for i in range(len(savedDomains)):              #Restore the domains if the assignment fails
                    coordinates[i].setDomain(savedDomains[i])
        raise NoSolution()
        #IF YOU GET PAST THIS FOR LOOP, IT MEANS NO ASSIGNMENTS TO A VARIABLE YIELDED A SOLUTION. GAME OVER, NO SOLUTION
                
        """
            if (len(coord.getDomain()) > 1):
                savedDomains = []
                #Find variable with smallest non-1 sized domain
                smallestDomainCoord = 
                smallestDomainCoord.
                for smallDomainCoord in coordinates:
                    if len(smallDomainCoord.getDomain()) != 1 
                            and len(smallDomainCoord.getDomain()) > len(smallestDomainCoord.getDomain()):
                        smallDomainCoord = smallDomainCoord
                for saveCoordinate in coordinates:
                    savedDomains.append(coordinate.deepcopy(saveCoordiante.getDomain()))
                for 
    """
    try:
        arcConsistencyHelper(board)
    except Solution:
        print("SOLUTION FOUND:")
        for i in range(board.getSize()):
            print("Column " + str(i))
            print("#########")
            for j in range(board.getSize()):
                print("(" + str(board.getCoordinate(i, j).getX()) + "," + 
                    str(board.getCoordinate(i, j).getY()) + "): " + str(board.getCoordinate(i, j).getDomain()[0]))
            print("") 
    except NoSolution:
        print("no solution found")



class Solution(Exception):
    def dummy():
        return #does nothing

class NoSolution(Exception):
    def dummy():
        return #does nothing

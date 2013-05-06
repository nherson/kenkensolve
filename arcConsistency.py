import itertools
import coordinate
from constraint import RCConstraint, ArithmeticConstraint

class arcConsistency():
    """
    Object to wrap around arcConsistency kenken solving interface.
    Contains methods and procedures needed to solve KenKens via
    arConsistency as a primary means of pruning domains
    """
    def __init__(self, board):
        #Just get a local copy of the coordinates, for convenience
        self.board = board
        self.coordinates = []
        for i in range(board.getSize()):
            for coord in board.getRow(i):
                self.coordinates.append(coord)
        #Initialize the Queue
        self.initializeConsistencyQueue()

    def initializeConsistencyQueue(self):
        #Add all (Coordiante, Constraint) pairs to the queue to start
        self.consistencyQueue = []
        for coord in self.coordinates:
            for constraint in coord.getConstraints():
                if (coord, constraint) not in self.consistencyQueue:
                    self.consistencyQueue.append((coord, constraint))
 
    def arcConsistencyHelper(self):
        """
        The helper function is recurses every time the queue is emptied,
        and a coordinate must be assigned a value.  When the helper function
        finds a solution, it throws a "Solution" exception, which immediately exits all
        recursion and is caught outside the helper function (neat!).
        """
        while (len(self.consistencyQueue) != 0):
            #Keep looping until all constraints are satisfied, and no more pruning is available
            currentCoordinate, currentConstraint = self.consistencyQueue.pop(0)
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
                    self.addRelatedToQueue(currentCoordinate)
            #When arcConsistencyHelper terminates, it returns and the board's coordinates and their domains 
            #have been modified.


    def solve(self):
        """
        Searches for a solution using a combination of arcConsistency
        and backtracking. The Algorithm will run arcConsistency,
        find the smallest remaining domain (that's greater than 1), and
        systematically assign a value to the variable and recurse onwards.
        Returns True is a solution is found, False otherwise.
        """
        self.arcConsistencyHelper()
        if self.isSolved():
            for coordinate in self.board.getCoordinates():
                coordinate.setValue(coordinate.getDomain()[0])
            return True
        elif self.isDeadEnd():
            return False
        else:
            print("selecting a variable to assign")
            savedDomains = self.backupDomains(self.getListOfDomains())
            smallest = self.indexOfSmallestDomain(savedDomains)
            for x in savedDomains[smallest]:
                self.addRelatedToQueue(self.coordinates[smallest])
                self.coordinates[smallest].setDomain([x,])
                if (self.solve()):
                    return True
                self.restoreDomains(self.backupDomains(savedDomains))
            else:
                return False 

    def solveWithLCV(self):
        """
        Works the same as solveWithBackTracking, but assigns the variable
        in an order such that you assign the least constraining value first.  
        That is, assign the value which would cause the least domain pruning 
        after running arcConsistency.
        """
        self.arcConsistencyHelper()
        if self.isSolved():
            for coordinate in self.board.getCoordinates():
                coordinate.setValue(coordinate.getDomain()[0])
            return True
        elif self.isDeadEnd():
            return False
        else:
            savedDomains = self.backupDomains(self.getListOfDomains())
            smallest = self.indexOfSmallestDomain(savedDomains)
            resultingDomainsList = []
            for x in savedDomains[smallest]:
                self.addRelatedToQueue(self.coordinates[smallest])
                self.coordinates[smallest].setDomain([x,])
                self.arcConsistencyHelper()
                resultingDomainsList.append((x, self.getListOfDomains()))
                self.restoreDomains(self.backupDomains(savedDomains))
            for assignment, resultingDomains in resultingDomainsList:
                for domain in resultingDomains:
                    if (len(domain) == 0):
                        resultingDomainsList.remove((assignment, resultingDomains)) #This assignment cannot work
                        break
            #compute resulting total domain sizes
            mappedTotalDomainSizes = list(map(self.totalSizeOfDomains, 
                                                [domains for assignment, domains in resultingDomainsList]))
            #pick the assigned variables, ordered by resulting domain size
            for i in range(len(resultingDomainsList)):
                currentAssignmentIndex = mappedTotalDomainSizes.index(max(mappedTotalDomainSizes))
                currentAssignment, currentDomains = resultingDomainsList[currentAssignmentIndex]
                self.restoreDomains(currentDomains)
                self.coordinates[smallest].setDomain([currentAssignment,])
                if (self.solveWithLCV()):
                    return True
            else:
                return False

    def totalSizeOfDomains(self, domains):
        totalSize = 0
        for domain in domains:
            totalSize += len(domain)
        return totalSize

    def getListOfDomains(self):
        domains = []
        for coord in self.coordinates:
            domains.append(coord.getDomain())
        return domains

    def backupDomains(self, domains):
        domainCopies = []
        for d in domains:
            domainCopies.append(coordinate.deepcopy(d))
        return domainCopies

    def restoreDomains(self, domains):
        for i in range(len(domains)):
            self.coordinates[i].setDomain(domains[i])

    def indexOfSmallestDomain(self, domains):
        smallest = None
        for i in range(len(domains)):
            if (smallest == None or ((len(domains[i]) > 1) and (len(domains[i]) > len(domains[smallest])))):
                smallest = i
        return smallest

    def isSolved(self):
        for domain in self.getListOfDomains():
            if (len(domain) != 1):
                return False
        return True

    def isDeadEnd(self):
        for domain in self.getListOfDomains():
            if (len(domain) == 0):
                return True
        return False

    def addRelatedToQueue(self, coord):
        for const in coord.getConstraints():
            for relatedCoord in const.getCoordinates():
                if (relatedCoord, const) not in self.consistencyQueue:
                    self.consistencyQueue.append((relatedCoord, const))


#Extensions of generic exceptions, used to take advantage
#of exception throwing to navigate around the code efficiently
class Solution(Exception):
    def dummy():
        return #does nothing

class NoSolution(Exception):
    def dummy():
        return #does nothing

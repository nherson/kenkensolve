
class Constraint:
    """
    #Abstract class defining constraint characteristics
    #def includesCoordinate(self, coordinate):
        #Returns True IFF constraint involves the given coordinate

    #def getCoordinates(self):
        #Returns list of coordinates involved with the constraint
    
    def isBroken(self):
        #Returns True IFF the values assigned to the coordinates 
        #within the constraint violate the constraint
    """

class RCConstraint(Constraint):
    #Constraints for having no duplicate numbers in the same row or column
    def __init__(self, board, coordinates):
        """
        rcNumber - number of row/column
        rc - string indicating whether its a row or column
        
        self.coordinates = []
        if (rc == 'r'):
            for coordinate in board.getRow(rcNumber):
                self.coordinates.append(coordinate)
        if (rc == 'c'):
            for coordinate in board.getColumn(rcNumber):
                self.coordinates.append(coordinate)
        """
        self.coordinates = coordinates
    def getCoordinates(self):
        return self.coordinates

    def includesCoordinate(self, coordinate):
        return (coordinate in self.getCoordinates())

    def isBroken(self):
           values = [coord.getValue() for coord in self.getCoordinates() if coord.getValue != None]
           return len(values) != len(set(values))

    def valuesSatisfyConstraint(self, values):
        if (len(values) != len(self.coordinates)):
            raise Exception("RCConstraint broken")
        return len(set(values)) == len(values)

class ArithmeticConstraint(Constraint):
    """
    Class representing arithmetic constraints on the kenken board.
    For example, spaces (0,0) and (1,0) must add to 4.
    Stores coordinates, the function which operates on those coordiantes
    """

    def __init__(self, func, result, coordinates):
        self.func = func
        self.coordinates = coordinates
        self.result = result
        
    def includesCoordinate(self, coordinate):
        return coordinate in self.getCoordinates()

    def getCoordinates(self):
        return self.coordinates

    def isBroken(self):
        values = [coord.getValue() for coord in self.getCoordinates()]
        return self.func(*values) != None and func(*values) != self.result

    def valuesSatisfyConstraint(self, values):
        if len(values) != len(self.coordinates):
            raise Exception("Not enough parameters to check constraint")
        return self.func(*values) == self.result

    
    






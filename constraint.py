
class Constraint:
    """
    Abstract class defining constraint characteristics
    """
    def includesCoordinate(self, coordinate):
        """
        Returns True IFF constraint involves the given coordinate
        """

    def getCoordinates(self):
        """
        Returns list of coordinates involved with the constraint
        """
    
    def isBroken(self):
        """
        Returns True IFF the values assigned to the coordinates 
        within the constraint violate the constraint
        """

class RCConstraint(Constraint):
    """
    Constraints that dictate every row having only one of each number
    in the set [1, board.getSize()].
    """
    def __init__(self, board, coordinates):
        """
        RCConstraints only need to be fed the coordinates with which they are involved
        This information implicitly tells you which row/column the constraint
        is maintaining.
        """
        self.coordinates = coordinates

    def getCoordinates(self):
        """
        Returns list of associated coordinates
        """
        return self.coordinates

    def includesCoordinate(self, coordinate):
        """
        Returns True IFF the constraint contains coordinate
        """
        return (coordinate in self.getCoordinates())

    def valuesSatisfyConstraint(self, values):
        """
        Given some series of values, returns True IFF the values given
        satisfy the constraint.  Order does not matter, because the constraint
        only cares whether or not there are duplicate values in the row/column
        """
        #start by sanity checking that there are enough values given
        if (len(values) != len(self.coordinates)):
            raise Exception("RCConstraint broken")
        return len(set(values)) == len(values) #True IFF values has no duplicates

class ArithmeticConstraint(Constraint):
    """
    Class representing arithmetic constraints on the kenken board.
    For example, spaces (0,0) and (1,0) might have to add to 4.
    Each ArithmeticConstraint must have an operation:
        - Add
        - Subtract
        - Multiply
        - Divide
        - Constant (giving you the answer for that square)
    As well as a result which the operation, applied to the values of the
    coordinates, should evaluate to.
    """
    def __init__(self, func, result, coordinates):
        self.func = func
        self.coordinates = coordinates
        self.result = result
        
    def includesCoordinate(self, coordinate):
        return coordinate in self.getCoordinates()

    def getCoordinates(self):
        return self.coordinates

    """
    Given some values, returns True IFF the values can be passed into
    the ArithmeticConstraint's operation function, and results in the
    proper evaluation result specified by the constraint in self.result
    """
    def valuesSatisfyConstraint(self, values):
        #Sanity check that the right number of values are given
        if len(values) != len(self.coordinates):
            raise Exception("Not enough parameters to check constraint")
        return self.func(*values) == self.result #Return True IFF constraint isn't broken

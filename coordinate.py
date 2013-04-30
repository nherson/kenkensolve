class Coordinate:
    """
    >>> c = Coordinate(3, 4, [1,2,3,4,5])
    >>> d = Coordinate(3, 4, [1,2,3,4,7])
    >>> c.removeFromDomain(2)
    >>> d.removeFromDomain(1)
    >>> (d.inDomain(2) and c.inDomain(1))
    True
    >>> (c.inDomain(2) or d.inDomain(1))
    False
    >> (c.getDomain() == [1,3,4,5] and d.getDomain() == [2,3,4,7])
    True
    """
    def __init__(self, x, y, domain):
        self.x = x
        self.y = y
        self.domain = deepcopy(domain)
        self.originalDomain = deepcopy(domain)
        self.constraints = []

    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def domainSize(self):
        return self.domain

    def getDomain(self):
        return self.domain

    def setDomain(self, values):
        self.domain = values
    
    """
    Returns True IFF value is in Coordinate's domain.
    """
    def inDomain(self, value):
        return value in self.domain

    """
    Removes value from domain.
    If values isn't in domain, this function does nothing
    """
    def removeFromDomain(self, value):
        if (value in self.domain):
            self.domain.remove(value)

    """
    When the coordinate was initiated, a deepcopy of the domain
    was stored in self.originalDomain.
    This function restores that domain as the true domain.
    Of course, the restored domain must also be a deepcopy, in case
    the domain needs to be restored yet again in the future.
    """
    def resetDomain(self):
        self.domain = deepcopy(self.originalDomain)
    
    """
    Returns a list of constraints in which this coordinate is involved in
    """
    def getConstraints(self):
        return self.constraints

    """
    Add an associated constraint to a coordinate.
    """
    def addConstraint(self, constraint):
        self.constraints.append(constraint)


"""
A basic function to make deep copies of lists.  
Comes in handy when you want to store away the original
domains of coordinates, in case you want to restore them 
at some point in the future.

For an example of where this is used, see arcConsistency(board)
in arcConsistency.py [it is utilized for backtracking]
"""
def deepcopy(items):
    newlist = []
    for item in items:
        newlist.append(item)
    return newlist

class Coordinate:
    """
    >>> c = Coordinate(3, 4, [1,2,3,4,5])
    >>> d = Coordinate(3, 4, [1,2,3,4,7])
    >>> c.removeFromDomain(2)
    >>> d.removeFromDomain(1)
    >>> (d.inDomain(2) and c.inDomain(1))
    True
    >>> c.getValue()
    >>> c.setValue(3)
    >>> d.setValue(4)
    >>> (c.inDomain(2) or d.inDomain(1))
    False
    >>> c.releaseValue()
    >>> d.releaseValue()
    >>> (c.getDomain() == [1,2,3,4,5] and d.getDomain() == [1,2,3,4,7])
    True
    """
    def __init__(self, x, y, domain):
        self.x = x
        self.y = y
        self.domain = deepcopy(domain)
        self.originalDomain = deepcopy(domain)
        self.value = None
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

    def inDomain(self, val):
        return val in self.domain

    def removeFromDomain(self, value):
        if (value in self.domain):
            self.domain.remove(value)

    def getValue(self):
        return self.value

    def setValue(self, value):
        if (value not in self.getDomain()):
            raise ValueError("Tried to assign " + str(value) + " to Coordinate ("
                    +str(self.getX())+","+str(self.getY())+"), whose domain is only " + str(self.getDomain()))
        else:
            self.value = value
        self.domain = [value]

    def releaseValue(self):
        self.value = None
        self.domain = deepcopy(self.originalDomain)

    def valueAssigned(self):
        return value != None

    def resetDomain(self):
        self.domain = self.originalDomain
    
    def getConstraints(self):
        return self.constraints

    def addConstraint(self, constraint):
        self.constraints.append(constraint)

#Deep copy function to make sure each Coordinate has its own 
#personal domain to edit
def deepcopy(items):
    newlist = []
    for item in items:
        newlist.append(item)
    return newlist

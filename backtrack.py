class BackTrack:
    def __init__(self, board):
        self.board = board
        self.coordinates = []
        for i in range(board.getSize()):
            for coord in board.getRow(i):
                self.coordinates.append(coord)

    def solve(self):
        def solveHelper(index):
            if (self.isSolved()):
                return True
            elif (self.isDeadEnd()):
                return False
            else:
                currentCoordinate = self.board.getCoordinates()[index]
                for value in currentCoordinate.getDomain():
                    currentCoordinate.setValue(value)
                    if (solveHelper(index+1)):
                        return True
                    else:
                        currentCoordinate.releaseValue()
                return False

        return solveHelper(0)

    def isSolved(self):
        for constraint in self.board.getConstraints():
            values = []
            for coord in constraint.getCoordinates():
                if (coord.getValue() == None):  
                    return False
                values.append(coord.getValue())
            if (not constraint.valuesSatisfyConstraint(values)):
                return False
        return True

    def isDeadEnd(self):
        for constraint in self.board.getConstraints():
            values = []
            for coordinate in constraint.getCoordinates():
                if (coordinate.getValue() == None):
                    break
                values.append(coordinate.getValue())
            else:
                if (not constraint.valuesSatisfyConstraint(values)):
                    return True
        return False

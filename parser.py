

def parseConstraint(line):
    """
    Takes in a constraint line from a KenKen layout file and returns a tuple representing the constraint:
        Input:
            line - String of text making up a constraint
        Output:
            Tuple of form (function, tuple_of_coordinates_involved_in_constraint)
    """
        

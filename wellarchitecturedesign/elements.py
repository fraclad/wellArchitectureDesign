import numpy as np

class Tubular:
    def __init__(self, name, inD, outD, weight, top, low, shoeSize = None, weigth = None, info = ""):
        self.name = name
        self.inD = inD
        self.outD = outD
        self.top = top
        self.low = low
        self.totalLength = self.top - self.low
        self.weight = weight
        self.info = info
        self.totalWeight = self.totalLength * self.weight
        self.thickness = self.outD - self.inD
        self.shoeSize = shoeSize
        self.shoeWidth = None
        if shoeSize is not None:
            self.shoeWidth = shoeSize - outD
        self.summary = "{0}\nID = {1} in\nOD = {2} in\nFrom {3} ft to {4} ft\nWeight = {5} lb/ft\nShoe = {6} in\n{7}".format(
            name, inD, outD, top, low, weight, shoeSize, info)

class Cement:
    def __init__(self, top, low, tub0, tub1):
        checkerRightWall = [tub0, tub1]
        whichTube = np.argmax([tub0.outD, tub1.outD])
        rightWall = checkerRightWall[whichTube].inD
        leftWall = min(tub0.outD, tub1.outD)
        self.horVals = np.array([leftWall, rightWall])
        self.topVals = [top, top]
        self.lowVals = [low, low]
        self.summary = "cement from\n{0} ft to {1}ft".format(top, low)
        

class Packer:
    def __init__(self, depth, inner_tubular, outer_tubular, packer_type="tubing"):
        """
        Initialize a packer
        
        Parameters:
        depth (float): The depth at which the packer is set
        inner_tubular (Tubular): The inner tubular (tubing or casing) the packer is attached to
        outer_tubular (Tubular): The outer tubular the packer seals against
        packer_type (str): Type of packer - "tubing" for tubing-to-casing or "casing" for casing-to-casing
        """
        self.depth = depth
        self.inner_tubular = inner_tubular
        self.outer_tubular = outer_tubular
        self.innerD = inner_tubular.outD    # Packer seals on inner tubular OD
        self.outerD = outer_tubular.inD     # Packer seals against outer tubular ID
        self.height = 75  # Standard packer height in feet
        self.top = depth - self.height/2
        self.bottom = depth + self.height/2
        self.type = packer_type
        
class Tubing(Tubular):
    """Tubing class inherits from Tubular but has a different default color"""
    def __init__(self, name, inD, outD, weight, top, low, **kwargs):
        super().__init__(name, inD, outD, weight, top, low, **kwargs)
        self.color = "#348ceb"  # Default blue color for tubing
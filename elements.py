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
    def __init__(self, depth, tubing, casing):
        """
        Initialize a packer
        
        Parameters:
        depth (float): The depth at which the packer is set
        tubing (Tubular): The tubing the packer is attached to
        casing (Tubular): The casing the packer seals against
        """
        self.depth = depth
        self.innerD = tubing.outD  # Packer seals on tubing OD
        self.outerD = casing.inD   # Packer seals against casing ID
        self.height = 40  # Standard packer height in feet
        self.top = depth - self.height/2
        self.bottom = depth + self.height/2
        
class Tubing(Tubular):
    """Tubing class inherits from Tubular but has a different default color"""
    def __init__(self, name, inD, outD, weight, top, low, **kwargs):
        super().__init__(name, inD, outD, weight, top, low, **kwargs)
        self.color = "#348ceb"  # Default blue color for tubing
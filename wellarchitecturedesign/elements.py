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
            # Calculate shoe width as the difference between shoeSize and outD
            # This determines how far the shoe extends outward
            self.shoeWidth = shoeSize - outD
            # Ensure shoeWidth is positive and reasonable
            if self.shoeWidth <= 0:
                self.shoeWidth = outD * 0.2  # Default to 20% of outD if shoeSize is too small
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

class OpenHole(Tubular):
    """OpenHole class inherits from Tubular but represents an open wellbore section with no shoe"""
    def __init__(self, name, diameter, weight, top, low, **kwargs):
        inD = diameter
        outD = diameter * 1.01 
        # this wont matter anyway bcs the visualize thickness is not the actual physical thickness for tubular elements
        # also "openhole" has no physical thickness, this is put just for consistency
        super().__init__(name, inD, outD, weight, top, low, shoeSize=None, **kwargs)
        self.color = "#9c3d2a"
        self.is_openhole = True
        self.summary = "{0}\nDiameter = {1} in\nDepth = {3} ft\n{4}".format(
            name, diameter, top, low, self.info)
import numpy as np

class Tubular:
    def __init__(self, name, inD, outD, weight, top, low, weigth = None, info = ""):
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
        self.summary = "{0}\nID = {1} in\nOD = {2} in\nFrom {3} ft to {4} ft\nWeight = {5} lb/ft\n{6}".format(
            name, inD, outD, top, low, weight, info)

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
    def __init__(self):
        pass
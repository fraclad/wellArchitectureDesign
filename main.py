import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 12


"""
may use manual rectangle creation rather than ax.vline when vizualizing ...
draw rectangle: https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Rectangle.html
add rectangle: https://matplotlib.org/stable/gallery/statistics/errorbars_and_boxes.html#sphx-glr-gallery-statistics-errorbars-and-boxes-py
"""
class tubular:
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

class cement:
    def __init__(self, top, low, tub0, tub1):
        checkerRightWall = [tub0, tub1]
        whichTube = np.argmax([tub0.outD, tub1.outD])
        rightWall = checkerRightWall[whichTube].inD
        leftWall = min(tub0.outD, tub1.outD)
        self.horVals = [leftWall, rightWall]
        self.topVals = [top, top]
        self.lowVals = [low, low]
        
class well:
    def __init__(self):
        self.tubulars = {}
        self.tubularsLeft = {}
        self.cements = {}
        self.largestTub = 0
        self.deepestTub = 0
        self.cementID = 0
       
    # may want to create rectangles here ...
    def addTubular(self, tub):
        try:
            assert tub.name not in self.tubulars.keys()
            self.tubulars[tub.name] = {"xy":np.array([tub.inD, tub.low]), "width":tub.thickness, "height":tub.totalLength, "outD": tub.outD, "summary": tub.summary, "low": tub.low}
            if tub.outD > self.largestTub:
                self.largestTub = tub.outD
            if tub.low > self.deepestTub:
                self.deepestTub = tub.low
        except:
            raise ValueError("Tubular names must be unique! that tubular has been added to this well")
            
    def addCement(self, cem):
        self.cements[self.cementID] = {"horVals": cem.horVals, "topVals": cem.topVals, "lowVals": cem.lowVals}
        self.cementID += 1
                    
    def visualize(self):
        stretchHorView = self.largestTub * 5
        self.fig, self.ax = plt.subplots(figsize = (10,10))
        # the tubulars
        for key, elem in self.tubulars.items():
            self.ax.add_patch(Rectangle(elem["xy"], elem["width"], elem["height"], color = "black"))
            self.ax.add_patch(Rectangle((-1*elem["xy"][0], elem["xy"][1]), -1*elem["width"], elem["height"], color = "black"))
            # showing tubular summaries
            xText = elem["outD"] + (0.075 * stretchHorView)
            yText = elem["low"] * 0.85 
            self.ax.text(xText, yText, elem["summary"], 
                         verticalalignment = "top", horizontalalignment = "left")
        # the cement intervals
        for key, elem in self.cements.items():
            self.ax.fill_between(elem["horVals"], elem["topVals"], elem["lowVals"])
            
        self.ax.set_ylabel("MD [ft]")
        self.ax.set_xlim([-10,stretchHorView])
        self.ax.set_ylim([0, self.deepestTub])
        self.ax.invert_yaxis()
        #plt.tight_layout()
        plt.show()

        
### test

t0 = tubular(name = "conductor", inD = 7.25, outD = 8, weight = 58, top = 0, low = 250)
t1 = tubular(name = "surface", inD = 6.25, outD = 6.75, weight = 47, top = 0, low = 2000)
t2 = tubular(name = "intermediate", inD = 5.5, outD = 5.75, weight = 39, top = 0, low = 3750, info = "this is very expensive!")
t3 = tubular(name = "production", inD = 4.75, outD = 5, weight = 39, top = 0, low = 5200)
c0 = cement(top = 100, low = 2000, tub0 = t0, tub1 = t1)

well0 = well()
well0.addTubular(t0)
well0.addTubular(t1)
well0.addTubular(t2)
well0.addTubular(t3)
well0.addCement(c0)
well0.visualize()

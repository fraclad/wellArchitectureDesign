import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from elements import Tubular, Cement
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 12
        
class well:
    def __init__(self, name = None):
        self.tubulars = {}
        self.cements = {}
        self.largestTub = 0
        self.deepestTub = 0
        self.cementID = 0
        self.showTubularSummary = True
        self.showCementSummary = True
        self.name = name
       
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
        self.cements[self.cementID] = {"horVals": cem.horVals, "topVals": cem.topVals, "lowVals": cem.lowVals, "summary": cem.summary}
        self.cementID += 1
        
    def hideTubularSummary(self):
        self.showTubularSummary = False
        
    def hideCementSummary(self):
        self.showCementSummary = False
                    
    def visualize(self):
        stretchHorView = self.largestTub * 5
        self.fig, self.ax = plt.subplots(figsize = (10,12))
        # the tubulars
        for key, elem in self.tubulars.items():
            self.ax.add_patch(Rectangle(elem["xy"], elem["width"], elem["height"], color = "black"))
            self.ax.add_patch(Rectangle((-1*elem["xy"][0], elem["xy"][1]), -1*elem["width"], elem["height"], color = "black"))
            # showing tubular summaries
            if self.showTubularSummary == True:
                xText = elem["outD"] + (0.075 * stretchHorView)
                yText = elem["low"] * 0.85 
                self.ax.text(xText, yText, elem["summary"], 
                             verticalalignment = "top", horizontalalignment = "left")
        # the cement intervals
        for key, elem in self.cements.items():
            self.ax.fill_between(elem["horVals"], elem["topVals"], elem["lowVals"], color = "#6b705c")
            self.ax.fill_between(-1*elem["horVals"], elem["topVals"], elem["lowVals"], color = "#6b705c")
            # showing cement summaries
            if self.showCementSummary == True:
                xText = elem["horVals"][1] + (0.4 * stretchHorView)
                yText = elem["lowVals"][1]
                self.ax.text(xText, yText, elem["summary"], 
                             verticalalignment = "top", horizontalalignment = "left", color = "#6b705c")
            
        self.ax.set_ylabel("MD [ft]")
        self.ax.set_xlim([-10,stretchHorView])
        self.ax.set_ylim([0, self.deepestTub])
        self.ax.invert_yaxis()
        plt.title(self.name, loc = "left")
        plt.tight_layout()
        plt.show()

        
### execute

t0 = Tubular(name = "conductor", inD = 7.25, outD = 8, weight = 58, top = 0, low = 250)
t1 = Tubular(name = "surface", inD = 6.25, outD = 6.75, weight = 47, top = 0, low = 2000)
t2 = Tubular(name = "intermediate", inD = 5.5, outD = 5.75, weight = 39, top = 0, low = 3750, info = "this is very expensive!")
t3 = Tubular(name = "production", inD = 4.75, outD = 5, weight = 39, top = 0, low = 5200)
t4 = Tubular(name = "liner", inD = 3.75, outD = 4, weight = 27, top = 4800, low = 6500)
c0 = Cement(top = 100, low = 2000, tub0 = t0, tub1 = t1)
c1 = Cement(top = 1800, low = 3750, tub0 = t2, tub1 = t1)
c2 = Cement(top = 3500, low = 5200, tub0 = t2, tub1 = t3)

well0 = well(name = "Test Well 001")
well0.addTubular(t0)
well0.addTubular(t1)
well0.addTubular(t2)
well0.addTubular(t3)
well0.addTubular(t4)
well0.addCement(c0)
well0.addCement(c1)
well0.addCement(c2)
#well0.hideCementSummary()
well0.visualize()

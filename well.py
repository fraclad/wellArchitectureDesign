import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 12
        
class well:
    def __init__(self, name = None, kop = None, bur = None, inc = None):
        self.tubulars = {}
        self.cements = {}
        self.largestTub = 0
        self.deepestTub = 0
        self.cementID = 0
        self.showTubularSummary = True
        self.showCementSummary = True
        self.name = name
        self.kop = kop
        self.bur = bur
        self.inc = inc
       
    def addTubular(self, tub):
        try:
            assert tub.name not in self.tubulars.keys()
            self.tubulars[tub.name] = {"xy":np.array([tub.inD, tub.low]), "width":tub.thickness, "height":tub.totalLength, 
                                       "outD": tub.outD, "summary": tub.summary, "low": tub.low, "shoeWidth":tub.shoeWidth}            
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
        stretchHorView = self.largestTub * 4
        stretchVerView = self.deepestTub * 1.1
        self.fig, self.ax = plt.subplots(figsize = (8.27, 11.69))
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
                xText = -elem["horVals"][1] - (0.4 * stretchHorView)
                yText = elem["lowVals"][1]
                self.ax.text(xText, yText, elem["summary"], 
                             verticalalignment = "top", horizontalalignment = "left", color = "#6b705c")
                
        # the shoes
        for key, elem in self.tubulars.items():
            if elem["shoeWidth"] is not None:
                vizShoeHeight = stretchVerView * 0.01
                p0 = [elem["outD"], elem["low"]]
                p1 = [elem["outD"], elem["low"] - vizShoeHeight]
                p2 = [elem["outD"] + elem["shoeWidth"], elem["low"]]
                shoe = plt.Polygon([p0, p1, p2], color = "black")
                self.ax.add_patch(shoe)
                p0[0] *= -1
                p1[0] *= -1
                p2 = [-elem["outD"] - elem["shoeWidth"], elem["low"]]
                shoe = plt.Polygon([p0, p1, p2], color = "black")
                self.ax.add_patch(shoe)
            
        self.ax.set_ylabel("MD [ft]")
        self.ax.set_xlim([-stretchHorView, stretchHorView])
        self.ax.set_ylim([0, stretchVerView])
        if self.kop is not None:
            kopColor = "#0C1713"
            self.ax.hlines(self.kop, -stretchHorView, stretchHorView, linestyle = "--", color = kopColor, linewidth = 0.5, alpha = 0.75,zorder=0)
            self.ax.annotate("KOP at {} ft".format(self.kop), xy = (-stretchHorView + 1, self.kop - 25), color = kopColor, alpha = 0.75)
        self.ax.invert_yaxis()
        plt.title(self.name, loc = "left")
        plt.tight_layout()
        plt.show()

        

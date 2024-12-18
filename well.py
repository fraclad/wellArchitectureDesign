import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from elements import Tubing  # Add import for Tubing class
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 12

class well:
    def __init__(self, name=None, topVerView=None, mdl=None, kop=None, bur=None, inc=None, 
                 verStretchFactor=1.05, horStretchFactor=4):
        self.tubulars = {}
        self.cements = {}
        self.packers = []  # New list to store packers
        self.tubing = None  # Store single tubing string
        self.largestTub = 0
        self.deepestTub = 0
        self.cementID = 0
        self.showTubularSummary = True
        self.showCementSummary = True
        self.name = name
        self.topVerView = topVerView
        self.mdl = mdl
        self.kop = kop
        self.bur = bur
        self.inc = inc
        self.verStretchFactor = verStretchFactor
        self.horStretchFactor = horStretchFactor

    def addTubular(self, tub):
        # Check if it's a tubing instance
        if isinstance(tub, Tubing):
            self.tubing = {"xy": np.array([tub.inD, tub.low]), 
                          "width": tub.thickness, 
                          "height": tub.totalLength,
                          "color": tub.color}
            return

        # Existing tubular handling code...
        try:
            assert tub.name not in self.tubulars.keys()
            self.tubulars[tub.name] = {
                "xy": np.array([tub.inD, tub.low]), 
                "width": tub.thickness, 
                "height": tub.totalLength,
                "outD": tub.outD, 
                "summary": tub.summary, 
                "low": tub.low, 
                "shoeWidth": tub.shoeWidth
            }
            if tub.outD > self.largestTub:
                self.largestTub = tub.outD
            if tub.low > self.deepestTub:
                self.deepestTub = tub.low
        except:
            raise ValueError("Tubular names must be unique! that tubular has been added to this well")

    def addPacker(self, packer):
        """Add a packer to the well"""
        self.packers.append({
            "depth": packer.depth,
            "innerD": packer.innerD,
            "outerD": packer.outerD,
            "top": packer.top,
            "bottom": packer.bottom
        })

    def addCement(self, cem):
        self.cements[self.cementID] = {
            "horVals": cem.horVals, 
            "topVals": cem.topVals, 
            "lowVals": cem.lowVals, 
            "summary": cem.summary
        }
        self.cementID += 1

    def hideTubularSummary(self):
        self.showTubularSummary = False

    def hideCementSummary(self):
        self.showCementSummary = False

    def visualize(self):
        stretchHorView = self.largestTub * self.horStretchFactor
        stretchVerView = self.deepestTub * self.verStretchFactor
        self.fig, self.ax = plt.subplots(figsize=(8.27, 11.69))

        # Draw tubulars
        for key, elem in self.tubulars.items():
            self.ax.add_patch(Rectangle(elem["xy"], elem["width"], elem["height"], color="black"))
            self.ax.add_patch(Rectangle((-1*elem["xy"][0], elem["xy"][1]), -1*elem["width"], elem["height"], color="black"))
            if self.showTubularSummary:
                xText = elem["outD"] + (0.075 * stretchHorView)
                yText = elem["low"] * 0.85
                self.ax.text(xText, yText, elem["summary"],
                           verticalalignment="top", horizontalalignment="left")

        # Draw cement
        for key, elem in self.cements.items():
            self.ax.fill_between(elem["horVals"], elem["topVals"], elem["lowVals"], color="#6b705c")
            self.ax.fill_between(-1*elem["horVals"], elem["topVals"], elem["lowVals"], color="#6b705c")
            if self.showCementSummary:
                xText = -elem["horVals"][1] - (0.4 * stretchHorView)
                yText = elem["lowVals"][1]
                self.ax.text(xText, yText, elem["summary"],
                           verticalalignment="top", horizontalalignment="left", color="#6b705c")

        # Draw shoes
        for key, elem in self.tubulars.items():
            if elem["shoeWidth"] is not None:
                vizShoeHeight = stretchVerView * 0.01
                p0 = [elem["outD"], elem["low"]]
                p1 = [elem["outD"], elem["low"] - vizShoeHeight]
                p2 = [elem["outD"] + elem["shoeWidth"], elem["low"]]
                shoe = plt.Polygon([p0, p1, p2], color="black")
                self.ax.add_patch(shoe)
                p0[0] *= -1
                p1[0] *= -1
                p2 = [-elem["outD"] - elem["shoeWidth"], elem["low"]]
                shoe = plt.Polygon([p0, p1, p2], color="black")
                self.ax.add_patch(shoe)

        # Draw tubing if present (single centered rectangle)
        if self.tubing:
            # Center the tubing at x=0
            tubing_half_width = self.tubing["width"] / 2
            self.ax.add_patch(Rectangle((-tubing_half_width, self.tubing["xy"][1]), 
                                      self.tubing["width"], 
                                      self.tubing["height"], 
                                      color=self.tubing["color"]))

        # Draw packers
        for packer in self.packers:
            # Draw packer on both sides (symmetric)
            for side in [1, -1]:
                x = side * packer["innerD"]
                width = side * (packer["outerD"] - packer["innerD"])
                height = packer["bottom"] - packer["top"]
                self.ax.add_patch(Rectangle((x, packer["top"]), width, height, 
                                          color="red", alpha=0.8))

        self.ax.set_ylabel("MD [ft]")
        self.ax.set_xlim([-stretchHorView, stretchHorView])
        if self.topVerView is None:
            self.ax.set_ylim([0, stretchVerView])
        else:
            self.ax.set_ylim([self.topVerView, stretchVerView])
        
        if self.kop is not None:
            kopColor = "#0C1713"
            self.ax.hlines(self.kop, -stretchHorView, stretchHorView, 
                         linestyle="--", color=kopColor, linewidth=0.5, alpha=0.75, zorder=0)
            self.ax.annotate(f"KOP at {self.kop} ft", 
                           xy=(-stretchHorView + 1, self.kop - 25), 
                           color=kopColor, alpha=0.75)

        if self.mdl is not None:
            mdlColor = "#348ceb"
            self.ax.hlines(self.mdl, -stretchHorView, stretchHorView, 
                         linestyle="--", color=mdlColor, linewidth=0.5, alpha=0.75, zorder=0)
            self.ax.annotate(f"Mudline at {self.mdl} ft", 
                           xy=(-stretchHorView + 1, self.mdl - 25), 
                           color=mdlColor, alpha=0.75)

        self.ax.invert_yaxis()
        plt.title(self.name, loc="left")
        plt.tight_layout()
        plt.show()
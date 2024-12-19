import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from elements import Tubing
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 8

class Well:
    def __init__(self, name=None, topVerView=None, mdl=None, kop=None, bur=None, inc=None, 
                 verStretchFactor=1.05, horStretchFactor=4):
        self.tubulars = {}
        self.cements = {}
        self.packers = []
        self.tubing = None
        self.largestTub = 0
        self.deepestTub = 0
        self.thicknesses = []
        self.minThickness = None
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
                          "width": tub.outD, 
                          "height": tub.totalLength,
                          "color": tub.color,
                          "outD": tub.outD}
            return

        try:
            assert tub.name not in self.tubulars.keys()
            thickness = tub.outD - tub.inD
            self.thicknesses.append(thickness)
            self.minThickness = min(self.thicknesses)
            
            self.tubulars[tub.name] = {
                "xy": np.array([tub.inD, tub.low]), 
                "centerline": (tub.outD + tub.inD) / 2,
                "width": thickness,
                "height": tub.totalLength,
                "outD": tub.outD, 
                "summary": tub.summary, 
                "low": tub.low,
                "top": tub.top,
                "shoeWidth": tub.shoeWidth,
                "inD": tub.inD,
                "name": tub.name  # Store name for reference
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
            "bottom": packer.bottom,
            "type": packer.type  # Add the packer type to the dictionary
        })

    def addCement(self, cem):
        self.cements[self.cementID] = {
            "horVals": cem.horVals, 
            "topVals": cem.topVals, 
            "lowVals": cem.lowVals, 
            "summary": cem.summary,
            "inner_wall": min(cem.horVals),
            "outer_wall": max(cem.horVals)
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

        # First draw cement (background)
        for key, cem in self.cements.items():
            # Find outer and inner casings
            outer_casing = None
            inner_casing = None
            
            for tub in self.tubulars.values():
                if abs(tub["outD"] - cem["inner_wall"]) < 0.01:
                    inner_casing = tub
                if abs(tub["inD"] - cem["outer_wall"]) < 0.01:
                    outer_casing = tub
            
            if inner_casing and outer_casing:
                # Calculate visual positions based on centerlines and minimum thickness
                inner_center = inner_casing["centerline"]
                outer_center = outer_casing["centerline"]
                
                # Calculate visual edges where cement should appear
                inner_visual_edge = inner_center + self.minThickness/2  # Outer edge of inner casing
                outer_visual_edge = outer_center - self.minThickness/2  # Inner edge of outer casing
                
                # Draw cement between visual edges of casings
                self.ax.fill_between([inner_visual_edge, outer_visual_edge], 
                                   cem["topVals"], cem["lowVals"], 
                                   color="#6b705c", zorder=1)
                self.ax.fill_between([-inner_visual_edge, -outer_visual_edge], 
                                   cem["topVals"], cem["lowVals"], 
                                   color="#6b705c", zorder=1)
                
                if self.showCementSummary:
                    xText = -outer_visual_edge - (0.4 * stretchHorView)
                    yText = cem["lowVals"][0]
                    self.ax.text(xText, yText, cem["summary"],
                               verticalalignment="top", horizontalalignment="left", color="#6b705c")

        # Draw tubulars
        for key, elem in self.tubulars.items():
            # Calculate the center position and visual outer edge of the casing
            center_pos = elem["centerline"]
            visual_outer_edge = center_pos + self.minThickness/2  # This is where the visible casing edge is
            
            # Draw casing with minimum thickness
            self.ax.add_patch(Rectangle((center_pos - self.minThickness/2, elem["xy"][1]), 
                                      self.minThickness, elem["height"], 
                                      color="black", zorder=2))
            self.ax.add_patch(Rectangle((-center_pos - self.minThickness/2, elem["xy"][1]), 
                                      self.minThickness, elem["height"], 
                                      color="black", zorder=2))
            
            # Draw shoe based on the visual outer edge
            if elem["shoeWidth"] is not None:
                vizShoeHeight = stretchVerView * 0.01
                # Right side shoe
                shoe_points = [
                    [visual_outer_edge, elem["low"]],  # Base point at visual casing edge
                    [visual_outer_edge, elem["low"] - vizShoeHeight],  # Top point
                    [visual_outer_edge + elem["shoeWidth"], elem["low"]]  # Tip point
                ]
                shoe = plt.Polygon(shoe_points, color="black", zorder=3)
                self.ax.add_patch(shoe)
                
                # Left side shoe (mirror)
                shoe_points_left = [
                    [-visual_outer_edge, elem["low"]],
                    [-visual_outer_edge, elem["low"] - vizShoeHeight],
                    [-(visual_outer_edge + elem["shoeWidth"]), elem["low"]]
                ]
                shoe = plt.Polygon(shoe_points_left, color="black", zorder=3)
                self.ax.add_patch(shoe)
            
            if self.showTubularSummary:
                xText = elem["outD"] + (0.075 * stretchHorView)
                yText = elem["low"] * 0.85
                self.ax.text(xText, yText, elem["summary"],
                           verticalalignment="top", horizontalalignment="left")

        # Draw tubing if present
        if self.tubing:
            tubing_half_width = self.tubing["width"] / 2
            self.ax.add_patch(Rectangle((-tubing_half_width, self.tubing["xy"][1]), 
                                      self.tubing["width"], 
                                      self.tubing["height"], 
                                      color=self.tubing["color"],
                                      zorder=2))

        # Draw packers - updated to handle both types
        if self.tubing:
            tubing_half_width = self.tubing["width"] / 2
        
        for packer in self.packers:
            if packer["type"] == "tubing":
                # Draw tubing-to-casing packer
                for side in [1, -1]:
                    x = side * tubing_half_width
                    width = side * (packer["outerD"] - tubing_half_width)
                    height = packer["bottom"] - packer["top"]
                    self.ax.add_patch(Rectangle((x, packer["top"]), width, height, 
                                            color="red", alpha=0.8, zorder=4))
            else:  # casing-to-casing packer
                # Find the casings involved
                inner_casing = None
                outer_casing = None
                for tub in self.tubulars.values():
                    if abs(tub["outD"] - packer["innerD"]) < 0.01:  # Inner casing
                        inner_casing = tub
                    if abs(tub["inD"] - packer["outerD"]) < 0.01:   # Outer casing
                        outer_casing = tub
                
                if inner_casing and outer_casing:
                    # Calculate visual positions
                    inner_center = inner_casing["centerline"]
                    outer_center = outer_casing["centerline"]
                    inner_visual_edge = inner_center + self.minThickness/2
                    outer_visual_edge = outer_center - self.minThickness/2
                    
                    # Draw casing-to-casing packer on both sides
                    for side in [1, -1]:
                        x = side * inner_visual_edge
                        width = side * (outer_visual_edge - inner_visual_edge)
                        height = packer["bottom"] - packer["top"]
                        self.ax.add_patch(Rectangle((x, packer["top"]), width, height,
                                                color="red", alpha=0.8, zorder=4))

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
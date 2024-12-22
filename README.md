# WellArchitectureDesign

A Python package for creating detailed well architecture diagrams and visualizations. This tool provides comprehensive well diagram generation capabilities with support for multiple tubular sections, cement visualization, and packer placement.

## Features

- Comprehensive tubular section visualization with customizable parameters
- Multiple cement section support with accurate representation
- Packer placement and visualization capabilities
- Automatic scaling and dimension handling
- Detailed component labeling and information display
- Support for complex well configurations

## Installation

Install using pip:

```bash
pip install wellarchitecturedesign
```

## Usage Example

Here's a complete example demonstrating the main features of the package:

```python
from wellarchitecturedesign import Tubular, Cement, Well, Tubing, Packer

# Define tubular sections
t0 = Tubular(name="conductor", inD=7.25, outD=8, weight=58, top=0, low=250)
t1 = Tubular(name="surface", inD=6.25, outD=6.75, weight=47, top=0, low=2000, shoeSize=7)
t2 = Tubular(name="intermediate", inD=5.5, outD=5.75, weight=39, top=0, low=3750, shoeSize=6, 
             info="this is very expensive!")
t3 = Tubular(name="production", inD=4.75, outD=5, weight=39, top=0, low=5200, shoeSize=5.25)
t4 = Tubular(name="liner", inD=3.75, outD=4, weight=27, top=4800, low=6500, shoeSize=4.5)

# Add tubing
tubing = Tubing(name="tubing", inD=2.75, outD=3.5, weight=15.5, top=0, low=6000)

# Define cement sections
c0 = Cement(top=0, low=2000, tub0=t0, tub1=t1)
c1 = Cement(top=1800, low=3750, tub0=t2, tub1=t1)
c2 = Cement(top=3500, low=5200, tub0=t2, tub1=t3)

# Add packers
p1 = Packer(depth=4000, inner_tubular=tubing, outer_tubular=t3, packer_type="tubing")
p2 = Packer(depth=5500, inner_tubular=tubing, outer_tubular=t4, packer_type="tubing")
p3 = Packer(depth=5000, inner_tubular=t4, outer_tubular=t3, packer_type="casing")

# Create and configure well
well = Well(name="Test Well 001", kop=5000)

# Add components to well
well.addTubular(t0)
well.addTubular(t1)
well.addTubular(t2)
well.addTubular(t3)
well.addTubular(t4)
well.addTubular(tubing)
well.addPacker(p1)
well.addPacker(p2)
well.addPacker(p3)

# Generate visualization
well.visualize()
```

This code generates:

![sample wellbore diagram output](https://raw.githubusercontent.com/fraclad/wellArchitectureDesign/ed44bbf331301fae5fa1118612315d8276c56ca6/plots/result2024Dec19.svg)

## Component Documentation

### Tubular
- `name`: Component identifier
- `inD`: Inner diameter (inches)
- `outD`: Outer diameter (inches)
- `weight`: Weight per foot (lb/ft)
- `top`: Starting depth (ft)
- `low`: Ending depth (ft)
- `shoeSize`: Shoe diameter (inches, optional)
- `info`: Additional information (optional)

### Cement
- `top`: Upper depth limit
- `low`: Lower depth limit
- `tub0`: Primary tubular component
- `tub1`: Secondary tubular component

### Packer
- `depth`: Installation depth
- `inner_tubular`: Interior tubular component
- `outer_tubular`: Exterior tubular component
- `packer_type`: Type specification ("tubing" or "casing")

### Well
- `name`: Well identifier
- `kop`: Kick-off point depth
- `topVerView`: Top view extent
- `mdl`: Mudline depth

## Requirements

- Python >=3.7
- numpy >=1.21.0
- matplotlib >=3.4.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Some Arguably Unnecessary Lore lol

I started this project because I had some free time in grad school, and this was never meant to be a full-fleshed project. I updated this project because I had some free time at work. If you think the structure of this project is messed-up, it was doomed from the get go ig lol


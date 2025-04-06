from wellarchitecturedesign import Tubular, Cement, Well, Tubing, Packer, OpenHole

# Define tubular sections
t0 = Tubular(name="conductor", inD=15, outD=15.5, weight=58, top=0, low=250)

open_hole_0 = OpenHole(name="open hole 0", diameter=14.5, weight=0, top=0, low=1975, 
                     info="uncased wellbore section0")
t1 = Tubular(name="surface", inD=13.5, outD=13.75, weight=47, top=0, low=2000, shoeSize =2)

open_hole_1 = OpenHole(name="open hole 1", diameter=13.5, weight=0, top=0, low=3725, 
                     info="uncased wellbore section1")
t2 = Tubular(name="intermediate", inD=12, outD=12.5, weight=39, top=0, low=3750, shoeSize=2, 
             info="this is very expensive!")

open_hole_2 = OpenHole(name="open hole 2", diameter=12, weight=0, top=0, low=5200, 
                     info="uncased wellbore section2")
t3 = Tubular(name="production", inD=9.5, outD=11, weight=39, top=0, low=5200, shoeSize=5.25)

open_hole_3 = OpenHole(name="open hole 3", diameter=5, weight=0, top=5200, low=6500, 
                     info="uncased wellbore section3")
t4 = Tubular(name="liner", inD=3.75, outD=4, weight=27, top=4800, low=6500, shoeSize=4.5)



# Add tubing
tubing = Tubing(name="tubing", inD=2.75, outD=3.5, weight=15.5, top=0, low=6000)

# Define cement sections
cc1 = Cement(top=0, low=2000, tub0=open_hole_0, tub1=t1)
c0 = Cement(top=0, low=3750, tub0=open_hole_1, tub1=t2)
c1 = Cement(top=2000, low=5200, tub0=open_hole_2, tub1=t3)

# Add packers
# p1 = Packer(depth=4000, inner_tubular=tubing, outer_tubular=t3, packer_type="tubing")
p2 = Packer(depth=5500, inner_tubular=tubing, outer_tubular=t4, packer_type="tubing")
p3 = Packer(depth=5000, inner_tubular=t4, outer_tubular=t3, packer_type="casing")

# Create and configure well
well = Well(name="Test Well with Open Hole")

# Add components to well
well.addTubular(t0)
well.addTubular(t1)
well.addTubular(t2)
well.addTubular(open_hole_0)
well.addTubular(open_hole_1)
well.addTubular(open_hole_2)
well.addTubular(open_hole_3)
well.addCement(cc1)
well.addCement(c0)
well.addCement(c1)
well.addTubular(t3)
well.addTubular(t4)
well.addTubular(tubing)
# well.addPacker(p1)
well.addPacker(p2)
well.addPacker(p3)

# Generate visualization
well.visualize()
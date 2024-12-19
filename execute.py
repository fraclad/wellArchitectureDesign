from elements import Tubular, Cement, Packer, Tubing
from well import well

# Existing tubulars
t0 = Tubular(name="conductor", inD=7.25, outD=8, weight=58, top=0, low=250)
t1 = Tubular(name="surface", inD=6.25, outD=6.75, weight=47, top=0, low=2000, shoeSize=7)
t2 = Tubular(name="intermediate", inD=5.5, outD=5.75, weight=39, top=0, low=3750, shoeSize=6, info="this is very expensive!")
t3 = Tubular(name="production", inD=4.75, outD=5, weight=39, top=0, low=5200, shoeSize=5.25)
t4 = Tubular(name="liner", inD=3.75, outD=4, weight=27, top=4800, low=6500, shoeSize=4.5)

# New tubing
tubing = Tubing(name="tubing", inD=2.75, outD=3.5, weight=15.5, top=0, low=6000)

# Cement sections
c0 = Cement(top=0, low=2000, tub0=t0, tub1=t1)
c1 = Cement(top=1800, low=3750, tub0=t2, tub1=t1)
c2 = Cement(top=3500, low=5200, tub0=t2, tub1=t3)

# Create packers
p1 = Packer(depth=4000, inner_tubular=tubing, outer_tubular=t3, packer_type="tubing")  # Tubing to production casing
p2 = Packer(depth=5500, inner_tubular=tubing, outer_tubular=t4, packer_type="tubing")  # Tubing to liner
p3 = Packer(depth=5000, inner_tubular=t4, outer_tubular=t3, packer_type="casing")      # Liner to production casing

# Create and configure well
well0 = well(name="Test Well 001", kop=5000)

# Add components
well0.addTubular(t0)
well0.addTubular(t1)
well0.addTubular(t2)
well0.addTubular(t3)
well0.addTubular(t4)
well0.addTubular(tubing)

# Add cement
well0.addCement(c0)
well0.addCement(c1)
well0.addCement(c2)

# Add packers
well0.addPacker(p1)
well0.addPacker(p2)
well0.addPacker(p3)  # New casing-to-casing packer

# Visualize
well0.visualize()
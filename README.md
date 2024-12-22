# WellArchitectureDesign

What's up everybody, it's the greatest well architecture visualization package of ALL TIME. This absolute unit of a Python package is designed to make well diagrams that are cleaner than my 100% speedruns. 

## Features That Go Crazy

Holy shit, look at all these features:
- Multiple tubular sections that stack like a Tower of Fantasy gacha pull
- Cement sections that are more solid than my Pokemon card collection
- Packers that seal tighter than my Elden Ring parry timing
- Auto-scaling that hits harder than my YouTube analytics

## Installation - Easy as Beating Pinwheel

Alright let's get this bad boy installed. It's easier than finding grass in Minecraft:

```bash
pip install wellarchitecturedesign
```

## The Most Insane Example of All Time

Check out this absolute banger of an example - it's going to blow your mind:

```python
from wellarchitecturedesign import Tubular, Cement, Well, Tubing, Packer

# Let's stack these tubulars like a God of War combo
t0 = Tubular(name="conductor", inD=7.25, outD=8, weight=58, top=0, low=250)
t1 = Tubular(name="surface", inD=6.25, outD=6.75, weight=47, top=0, low=2000, shoeSize=7)
t2 = Tubular(name="intermediate", inD=5.5, outD=5.75, weight=39, top=0, low=3750, shoeSize=6, 
             info="this is very expensive!")  # Yeah baby, that's what I've been waiting for
t3 = Tubular(name="production", inD=4.75, outD=5, weight=39, top=0, low=5200, shoeSize=5.25)
t4 = Tubular(name="liner", inD=3.75, outD=4, weight=27, top=4800, low=6500, shoeSize=4.5)

# Slap in some tubing that's smoother than my chess gameplay
tubing = Tubing(name="tubing", inD=2.75, outD=3.5, weight=15.5, top=0, low=6000)

# Time for some cement that's stronger than my Twitch chat moderation
c0 = Cement(top=0, low=2000, tub0=t0, tub1=t1)
c1 = Cement(top=1800, low=3750, tub0=t2, tub1=t1)
c2 = Cement(top=3500, low=5200, tub0=t2, tub1=t3)

# Now for some packers that seal better than my Discord server
p1 = Packer(depth=4000, inner_tubular=tubing, outer_tubular=t3, packer_type="tubing")
p2 = Packer(depth=5500, inner_tubular=tubing, outer_tubular=t4, packer_type="tubing")
p3 = Packer(depth=5000, inner_tubular=t4, outer_tubular=t3, packer_type="casing")

# Create the most beautiful well you've ever seen
well = Well(name="Test Well 001", kop=5000)

# Stack everything like we're building in Minecraft
well.addTubular(t0)
well.addTubular(t1)
well.addTubular(t2)
well.addTubular(t3)
well.addTubular(t4)
well.addTubular(tubing)
well.addPacker(p1)
well.addPacker(p2)
well.addPacker(p3)

# Let's see this masterpiece
well.visualize()
```

The code above generates:

!(sample wellbore diagram output)[https://raw.githubusercontent.com/fraclad/wellArchitectureDesign/ed44bbf331301fae5fa1118612315d8276c56ca6/plots/result2024Dec19.svg]

## Component Stats (Like a Character Build Screen)

### Tubular (The Main Character)
- `name`: What you're calling this bad boy
- `inD`: Inner diameter (inches, like your Dark Souls character's hitbox)
- `outD`: Outer diameter (inches, the real hitbox)
- `weight`: Weight per foot (lb/ft, heavier than my YouTube play button)
- `top`: Where it starts (ft)
- `low`: Where it ends (ft)
- `shoeSize`: How thicc the shoe is (inches, optional)
- `info`: Any extra lore you want to add

### Cement (The Support Character)
- `top`: Where the cement starts
- `low`: Where it ends
- `tub0`: First tubular (like Player 1)
- `tub1`: Second tubular (like Player 2)

### Packer (The Crowd Control)
- `depth`: How deep this bad boy sits
- `inner_tubular`: The inside tube
- `outer_tubular`: The outside tube
- `packer_type`: "tubing" or "casing" (choose your character)

### Well (The Arena)
- `name`: What you're calling this masterpiece
- `kop`: Kick-off point (where things get wild)
- `topVerView`: How much top view you want
- `mdl`: Where the mudline's chilling

## System Requirements (Minimum Specs)

This beast runs on:
- Python >=3.7 (like having a decent gaming PC)
- numpy >=1.21.0 (the graphics card)
- matplotlib >=3.4.0 (the RGB lighting)

## Contributing

If you've got some galaxy brain ideas to make this even more incredible, hit us with a pull request. Just make sure your code is cleaner than my Overwatch stats.

## License

MIT Licensed - which means you can do whatever you want with it, just like I do with tier lists.

That's about it, baby! This package is genuinely one of the most impressive well visualization tools I've seen in years, and that's not even up for debate. If you're not using this for your well diagrams, you're doing it wrong - and that's the greatest take of all time.

from elements import Tubular, Cement
from well import well


t0 = Tubular(name = "conductor", inD = 7.25, outD = 8, weight = 58, top = 0, low = 250)
t1 = Tubular(name = "surface", inD = 6.25, outD = 6.75, weight = 47, top = 0, low = 2000)
t2 = Tubular(name = "intermediate", inD = 5.5, outD = 5.75, weight = 39, top = 0, low = 3750, info = "this is very expensive!")
t3 = Tubular(name = "production", inD = 4.75, outD = 5, weight = 39, top = 0, low = 5200)
t4 = Tubular(name = "liner", inD = 3.75, outD = 4, weight = 27, top = 4800, low = 6500)
c0 = Cement(top = 100, low = 2000, tub0 = t0, tub1 = t1)
c1 = Cement(top = 1800, low = 3750, tub0 = t2, tub1 = t1)
c2 = Cement(top = 3500, low = 5200, tub0 = t2, tub1 = t3)

well0 = well(name = "Test Well 001", kop = 5000)
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

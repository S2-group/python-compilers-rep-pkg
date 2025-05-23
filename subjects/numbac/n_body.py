from numba import njit, float64
from numba.experimental import jitclass
from math import sqrt
import sys


PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

spec = [
    ('x', float64),
    ('y', float64),
    ('z', float64),
    ('vx', float64),
    ('vy', float64),
    ('vz', float64),
    ('mass', float64)
]

@jitclass(spec)
class Body:
  def __init__(self, x, y, z, vx, vy, vz, mass):
    self.x = x
    self.y = y 
    self.z = z    
    self.vx = vx
    self.vy = vy 
    self.vz = vz  
    self.mass = mass   

@njit
def offset_momentum(bodies):
  px, py, pz = 0.0, 0.0, 0.0        
  for b in bodies:                  
    px += b.vx * b.mass             
    py += b.vy * b.mass             
    pz += b.vz * b.mass             
                                    
  b = bodies[0]                     
  b.vx = - px / SOLAR_MASS          
  b.vy = - py / SOLAR_MASS          
  b.vz = - pz / SOLAR_MASS          

@njit
def energy(bodies):
  e = 0.0  
  num_bodies = len(bodies)  
  for i in range(num_bodies):  
    b = bodies[i]
    sq = b.vx * b.vx + b.vy * b.vy + b.vz * b.vz  
    e += 0.5 * bodies[i].mass * sq
    for j in range(i+1, num_bodies):  
      dx = b.x - bodies[j].x 
      dy = b.y - bodies[j].y 
      dz = b.z - bodies[j].z   
      sq = dx * dx + dy * dy + dz * dz 
      e -= (b.mass * bodies[j].mass) / sqrt(sq)   
  return e    

@njit
def advance(bodies, dt):
  num_bodies = len(bodies)
  for i in range(num_bodies): 
    for j in range(i+1, num_bodies):   
      dx = bodies[i].x - bodies[j].x 
      dy = bodies[i].y - bodies[j].y 
      dz = bodies[i].z - bodies[j].z       
      dpos_norm_sq = dx**2 + dy**2 + dz**2  
      mag = dt / (dpos_norm_sq * sqrt(dpos_norm_sq)) 
      
      mj = bodies[j].mass * mag
      bodies[i].vx -= dx * mj  
      bodies[i].vy -= dy * mj   
      bodies[i].vz -= dz * mj 
      
      mi = bodies[i].mass * mag      
      bodies[j].vx += dx * mi  
      bodies[j].vy += dy * mi   
      bodies[j].vz += dz * mi            
      
  for i in range(num_bodies): 
    bodies[i].x += bodies[i].vx * dt  
    bodies[i].y += bodies[i].vy * dt   
    bodies[i].z += bodies[i].vz * dt  

@njit
def main(n):
  bodies = [
    Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS),
    
    Body(
      4.84143144246472090e+00,
      -1.16032004402742839e+00,
      -1.03622044471123109e-01,
      1.66007664274403694e-03 * DAYS_PER_YEAR,
      7.69901118419740425e-03 * DAYS_PER_YEAR,
      -6.90460016972063023e-05 * DAYS_PER_YEAR,
      9.54791938424326609e-04 * SOLAR_MASS
      ),
    
    Body(
      8.34336671824457987e+00,
      4.12479856412430479e+00,
      -4.03523417114321381e-01,      
      -2.76742510726862411e-03 * DAYS_PER_YEAR,
      4.99852801234917238e-03 * DAYS_PER_YEAR,
      2.30417297573763929e-05 * DAYS_PER_YEAR,
      2.85885980666130812e-04 * SOLAR_MASS 
      ),    
    
    Body(
      1.28943695621391310e+01,
      -1.51111514016986312e+01,
      -2.23307578892655734e-01,
      2.96460137564761618e-03 * DAYS_PER_YEAR,
      2.37847173959480950e-03 * DAYS_PER_YEAR,
      -2.96589568540237556e-05 * DAYS_PER_YEAR,
      4.36624404335156298e-05 * SOLAR_MASS 
      ),    
    
    Body(
      1.53796971148509165e+01,
      -2.59193146099879641e+01,
      1.79258772950371181e-01,    
      2.68067772490389322e-03 * DAYS_PER_YEAR,
      1.62824170038242295e-03 * DAYS_PER_YEAR,
      -9.51592254519715870e-05 * DAYS_PER_YEAR,
      5.15138902046611451e-05 * SOLAR_MASS 
      )
    ]    
   
  offset_momentum(bodies)   
  print(float(int(energy(bodies) * 10**9)) / 10**9)
  for i in range(n):
    advance(bodies, 0.01)
  print(float(int(energy(bodies) * 10**9)) / 10**9)

if __name__ == '__main__':
  main(int(sys.argv[1]))
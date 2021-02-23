import math
import numpy as np
import matplotlib.pyplot as plt

class Astro:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.momentum = mass*position
        
def grav_force(astro1, astro2):
    dist_vec = astro1.position - astro2.position
    mag_dist_vec = np.sqrt(np.sum(np.square(dist_vec)))
    force_mag = - (G*(astro1.mass)*(astro2.mass)/(mag_dist_vec)**3.)
    force_vec = force_mag * dist_vec
    
    return force_vec

#Reading the data:
masses, init_pos_x, init_pos_y, init_pos_z, init_vel_x, init_vel_y, init_vel_z = np.loadtxt("SolarSystemData.txt", skiprows = 4, unpack = True)

#Gravitational constant
G = 8.88707e-10

#Objects indices: Sun -> S, Mercury -> Me, Venus -> V, Earth -> E, Mars -> M
#Units: distances AU, velocities AU/day, masses -> Earth masses, G -> AU^-3 . m_E^-1 . days^-2

#Sun's initial postion and velocity vectors and mass:
init_pos_S = np.array([ init_pos_x[0], init_pos_y[0], init_pos_z[0] ])
init_vel_S = np.array([ init_vel_x[0], init_vel_y[0], init_vel_z[0] ])
mass_S = masses[0]

#Mercury's initial position and velocity vectors and mass:
init_pos_Me = np.array([ init_pos_x[1], init_pos_y[1], init_pos_z[1] ])
init_vel_Me = np.array([ init_vel_x[1], init_vel_y[1], init_vel_z[1] ])
mass_Me = masses[1]

#Venus' initial position and velocity vectors and mass:
init_pos_V = np.array([ init_pos_x[2], init_pos_y[2], init_pos_z[2] ])
init_vel_V = np.array([ init_vel_x[2], init_vel_y[2], init_vel_z[2] ])
mass_V = masses[2]

#Earth's inital position and velocity vectors and mass:
init_pos_E = np.array([ init_pos_x[3], init_pos_y[3], init_pos_z[3] ])
init_vel_E = np.array([ init_vel_x[3], init_vel_y[3], init_vel_z[3] ])
mass_E = masses[3]

#Mars' initial position and velocity vectors and mass:
init_pos_M = np.array([ init_pos_x[4], init_pos_y[4], init_pos_z[4] ])
init_vel_M = np.array([ init_vel_x[4], init_vel_y[4], init_vel_z[4] ])
mass_M = masses[4]

#Creating objects:
Sun = Astro(mass_S, init_pos_S, init_vel_S)
Mercury = Astro(mass_Me, init_pos_Me, init_vel_Me)
Venus = Astro(mass_V, init_pos_V, init_vel_V)
Earth = Astro(mass_E, init_pos_E, init_vel_E)
Mars = Astro(mass_M, init_pos_M, init_vel_M)


dt = 0.001
t = 0.

while(True):

        #Calculating resultant forces on each objects:
        Sun_forceR = grav_force(Sun, Mercury) + grav_force(Sun, Venus) + grav_force(Sun, Earth) + grav_force(Sun, Mars)
        Mercury_forceR = grav_force(Mercury, Sun) + grav_force(Mercury, Venus) + grav_force(Mercury, Earth) + grav_force(Mercury, Mars)
        Venus_forceR = grav_force(Venus, Sun) + grav_force(Venus, Mercury) + grav_force(Venus, Earth) + grav_force(Venus, Mars)
        Earth_forceR = grav_force(Earth, Sun) + grav_force(Earth, Mercury) + grav_force(Earth, Venus) + grav_force(Earth, Mars)
        Mars_forceR = grav_force(Mars, Sun) + grav_force(Mars, Mercury) + grav_force(Mars, Venus) + grav_force(Mars, Earth)
        
        



        
    





















import numpy as np
import sys


class Astro:
    def __init__(self, mass, position, velocity, index):
        self.index = int(index)
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.momentum = mass*velocity


#Function responsible for the calculation of Gravitaional Force
def grav_force(astro1, astro2):
    G = 9.10677e-10            #Gravitational constant
    dist_vec = astro2.position - astro1.position
    dist_vec_mag = np.sqrt(np.sum(dist_vec ** 2))
    force_mag = (G*(astro1.mass)*(astro2.mass))/(dist_vec_mag**3)
    force_vec = - force_mag * dist_vec
    np.reshape(force_vec, 3)
    
    return force_vec      #Returns gravitational force on astro2 by astro1


#Units: distances - AU, velocities - AU/day, masses - Earth masses, G - AU^3 . m_E^-1 . days^-2

#Reading the data:
datafile = "/home/nicholassouza/PyProgs/NcorposSistemaSolar/Simulations/InitialConditions/" + input("Get data from: ")
objects_indices, masses, init_position_x, init_position_y, init_position_z, init_velocity_x, init_velocity_y, init_velocity_z = np.loadtxt(datafile, unpack = True)

number_of_objects = len(objects_indices)

#Real data from https://ssd.jpl.nasa.gov/horizons.cgi#results


#Organizing the inital data into vectors:
init_position_vectors = np.stack((init_position_x, init_position_y, init_position_z), axis=1)
init_velocity_vectors = np.stack((init_velocity_x, init_velocity_y, init_velocity_z), axis=1)


#Creating Astro objects:
astros = np.zeros(number_of_objects, dtype = Astro )    
for i in range(0, number_of_objects):
    astros[i] = Astro( masses[i], init_position_vectors[i], init_velocity_vectors[i], objects_indices[i] )


#Setting tsop and dt via terminal:
tstop = float(sys.argv[1]) 
dt = float(sys.argv[2]) 


t = 0.
step = 0
filenumber = 0
while(t <= tstop):
    
    t = step*dt
   
    #Computing resultant forces on each astro:
   
    for i in range(0, number_of_objects):
        resultant_force_on_i = np.zeros(3)
        
        for j in range(0, number_of_objects):
            if (i != j):
                resultant_force_on_i = resultant_force_on_i + grav_force( astros[j], astros[i] )

    	#Updating astros' atributes - Euler's Method:

        #Updating momentum:
        astros[i].momentum = astros[i].momentum + ( resultant_force_on_i * dt )
        
        #Updating velocities:
        astros[i].velocity = astros[i].momentum / astros[i].mass
        
        #Updating positions:
        astros[i].position = astros[i].position + ( astros[i].velocity * dt )
        
    step = step + 1
    
    #Saving data into text file:  (1 txt file per 1/dt iterations)
    frequency = 500                 #Change in order to get different frame rate.                
    if (step % frequency == 0):      
        
        #Getting back updated position_axis and velocity_axis arrays:
        position_x = np.zeros(number_of_objects)
        position_y = np.zeros(number_of_objects)
        position_z = np.zeros(number_of_objects)
        velocity_x = np.zeros(number_of_objects)
        velocity_y = np.zeros(number_of_objects)
        velocity_z = np.zeros(number_of_objects)
        for i in range(0, number_of_objects):
            position_x[i] = astros[i].position[0]
            position_y[i] = astros[i].position[1]
            position_z[i] = astros[i].position[2]
            velocity_x[i] = astros[i].velocity[0]
            velocity_y[i] = astros[i].velocity[1]
            velocity_z[i] = astros[i].velocity[2]
        
        
        #Getting txt files:
        filename = "file{}.txt".format(filenumber)
        
        info = "Output data from 3dSolarSystem.py"
        info += "\nSolar System - Rocky planets and Sun"
        info += "Time: t = {}".format(round(t, 3))
        info += "\n\n     masses           position_x           position_y           position_z           velocity_x           velocity_y           velocity_z"           

        np.savetxt("/home/nicholassouza/PyProgs/NcorposSistemaSolar/Simulations/Outputs/TextFiles/{}".format(filename), list(zip(masses, position_x, position_y, position_z, velocity_x, velocity_y, velocity_z)), header = info, fmt = "%20.8e")
        filenumber = filenumber + 1
        
        print("{} DONE".format(filename))
        
    

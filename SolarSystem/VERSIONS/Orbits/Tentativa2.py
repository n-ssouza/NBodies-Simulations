import numpy as np


class Astro:
    def __init__(self, mass, position, velocity, index):
        self.index = int(index)
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.momentum = mass*velocity


def grav_force(astro1, astro2):
    G = 8.88707e-10             #Gravitational constant
    dist_vec = astro1.position - astro2.position
    mag_dist_vec = np.sqrt(np.sum(np.square(dist_vec)))
    force_mag = - (G*(astro1.mass)*(astro2.mass)/(mag_dist_vec)**3.)
    force_vec = force_mag * dist_vec
    np.reshape(force_vec, (1,3))
    
    return force_vec


#Units: distances - AU, velocities - AU/day, masses - Earth masses, G - AU^-3 . m_E^-1 . days^-2

#Reading the data:
datafile = str(input("Get data from: "))
objects_indices, masses, position_x, position_y, position_z, velocity_x, velocity_y, velocity_z = np.loadtxt(datafile, unpack = True)

number_of_objects = len(objects_indices)


dt = 0.001
t = 0.
while(t <= 365):
    
    #Position vectors:
    position_vectors = np.zeros([number_of_objects, 3])
    for i in range(0, number_of_objects):
        position_vectors[i] = np.array([ position_x[i], position_y[i], position_z[i] ])
   

    #Velocity vectors:
    velocity_vectors = np.zeros([number_of_objects, 3])
    for i in range(0, number_of_objects):
        velocity_vectors[i] = np.array([ velocity_x[i], velocity_y[i], velocity_z[i] ])


    #Creating Objects:
    astros = np.zeros([number_of_objects, 1], dtype = Astro )
    for i in range(0, number_of_objects):
        astros[i] = Astro( masses[i], position_vectors[i], velocity_vectors[i], objects_indices[i] )


    #Computing resultant forces on each astro:
    resultant_force_on_i = np.zeros([1, 3])
    resultant_forces = np.zeros([number_of_objects, 3])
    for i in range(0, number_of_objects):
        for j in range(0, number_of_objects):
            if (astros[i, 0].index != astros[j, 0].index):
                resultant_force_on_i = resultant_force_on_i + grav_force( astros[i, 0], astros[j, 0] ) 
 
        resultant_forces[i] = resultant_force_on_i


    #Updating momenta vectors (atributes):
    for i in range(0, number_of_objects):
        astros[i, 0].momentum = astros[i, 0].momentum + resultant_forces[i] * dt


    #Updating position vectors (atributes and position_vectors):
    for i in range(0, number_of_objects):
        astros[i, 0].position = astros[i, 0].position + (astros[i, 0].momentum / astros[i, 0].mass) * dt
        position_vectors[i] = astros[i, 0].position
        
    
    #Updating velocity vectors (atributes and velocity_vectors):
    for i in range(0, number_of_objects):
        astros[i, 0].velocity = astros[i, 0].momentum / astros[i, 0].mass
        velocity_vectors[i] = astros[i, 0].velocity


    #Getting back new position_axis and velocity_axis arrays:
    position_x = np.zeros(number_of_objects)
    position_y = np.zeros(number_of_objects)
    position_z = np.zeros(number_of_objects)
    for i in range(0, number_of_objects):
        position_x[i] = position_vectors[i, 0]
    for i in range(0, number_of_objects):
        position_y[i] = position_vectors[i, 1]
    for i in range(0, number_of_objects):
        position_z[i] = position_vectors[i, 2]
    
    velocity_x = np.zeros(number_of_objects)
    velocity_y = np.zeros(number_of_objects)
    velocity_z = np.zeros(number_of_objects)
    for i in range(0, number_of_objects):
        velocity_x[i] = velocity_vectors[i, 0]
    for i in range(0, number_of_objects):
        velocity_y[i] = velocity_vectors[i, 1]
    for i in range(0, number_of_objects):
        velocity_z[i] = velocity_vectors[i, 2]
    
    t = t + dt
    
    
    #Saving data into text file: a file per day - 1 .txt per 1000 iterations
    if (t in range(0, 366)):

        filename = "day-" + str(int(t)) + ".txt"
    
        info = "Output data from 3dSolarSystem.py"
        info += "\nSolar System - Rocky planets and Sun"
        info += "Time: t = " + str(t)
        info += "\n\n      position_x           position_y           position_z"
    
        np.savetxt(filename, list(zip(position_x, position_y, position_z)), header = info, fmt = "%20.8e")




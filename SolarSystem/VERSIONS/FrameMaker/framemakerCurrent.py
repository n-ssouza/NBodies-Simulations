import sys
import numpy as np
import matplotlib.pyplot as plt


def plot_orbits(fig_orbits, ax1, ax2, time, positions_x, positions_y):
 
    fig_orbits.suptitle('Rocky Solar System Orbits: t = {}'.format(time), fontsize = 16)   
 
    ax1.cla()
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-2.5, 2.5)
    ax1.set_xlabel('X (AU)')
    ax1.set_ylabel('Y (AU)')
    ax1.set_aspect('equal')
    
    ax2.set_xlim(-2.5, 2.5)
    ax2.set_ylim(-2.5, 2.5)
    ax2.set_xlabel('X (AU)')
    ax2.set_aspect('equal')
    
    base_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    for i in range(0, number_of_objects): 
        ax1.plot(positions_x[i], positions_y[i], base_colors[i]+'o', markersize = 1.3)
        ax2.plot(positions_x[i], positions_y[i], base_colors[i]+'o', markersize = 1.3)

    fig_orbits.savefig("/home/nicholassouza/PyProgs/NcorposSistemaSolar/Simulations/Outputs/Frames/Orbits/{}".format(framename), dpi=250)


def plot_energy(fig_energy, ax1, ax2, time, InitialEnergy, TotalKineticEnergy, TotalPotentialEnergy):

    fig_energy.suptitle('Rocky Solar System - Conservation of energy and Virial Ratio')

    ax1.set_xlim(0, 365)
    ax1.set_ylim(-0.05, 0.05)
    ax1.set_xlabel('Time (days)')
    ax1.set_ylabel('(Et-E0)/E0')
    ax1.axhline(color="gray", zorder=-1)
    ax1.set_aspect('auto')
    
    ax2.set_xlim(0, 365)
    ax2.set_ylim(0, 2.0)
    ax2.set_xlabel('Time (days)')
    ax2.set_ylabel('-2T/U')
    ax2.axhline(y = 1.0, color="gray", zorder=-1)
    ax2.set_aspect('auto')

    TotalEnergy = TotalKineticEnergy + TotalPotentialEnergy

    ax1.plot(time, (TotalEnergy-InitialEnergy)/InitialEnergy, 'bo', markersize = 1.0)
    ax2.plot(time, -2.0*TotalKineticEnergy/TotalPotentialEnergy, 'bo', markersize = 1.0)

    fig_energy.savefig("/home/nicholassouza/PyProgs/NcorposSistemaSolar/Simulations/Outputs/Frames/Energy/{}".format(framename), dpi=250)


number_of_frames = int(sys.argv[1])

fig_orbits, (ax_orbits1, ax_orbits2) = plt.subplots(nrows=1, ncols=2, constrained_layout = True)
fig_energy, (ax_energy1, ax_energy2) = plt.subplots(nrows=1, ncols=2, constrained_layout = True)

framenumber = 0
tstart = 0.0
dt = 0.5
G = 9.10677e-10
while(framenumber <= number_of_frames):

    datafile = "/home/nicholassouza/PyProgs/NcorposSistemaSolar/Simulations/Outputs/TextFiles/file{}.txt".format(framenumber)
    framename = "frame{}.png".format(framenumber)
    

    masses, positions_x, positions_y, positions_z, velocity_x, velocity_y, velocity_z = np.loadtxt(datafile, unpack = True)
    number_of_objects = len(positions_x)

    position_vectors = np.stack((positions_x, positions_y, positions_z), axis=1)
    velocities = np.stack((velocity_x, velocity_y, velocity_z), axis=1)
    velocities_mag = np.linalg.norm(velocities, axis=1)


    TotalKineticEnergy = np.dot(0.5*masses, np.square(velocities_mag))

    TotalPotentialEnergy = 0.0
    for i in range(0, number_of_objects):
        for j in range(0, number_of_objects):
                if (j > i):
                    TotalPotentialEnergy = TotalPotentialEnergy + (masses[i]*masses[j]) / np.sqrt(np.sum(np.square(position_vectors[j] - position_vectors[i])))  

    TotalPotentialEnergy = -G*TotalPotentialEnergy


    if framenumber == 0:
    	InitialEnergy = TotalKineticEnergy + TotalPotentialEnergy


    time = tstart + framenumber*dt

    #plot_orbits(fig_orbits, ax_orbits1, ax_orbits2, time, positions_x, positions_y)
    #print("frame_orbits{}".format(framenumber), "DONE") 

    plot_energy(fig_energy, ax_energy1, ax_energy2, time, InitialEnergy, TotalKineticEnergy, TotalPotentialEnergy)
    print("frame_energy{}".format(framenumber), "DONE")

   
    framenumber = framenumber + 1
    
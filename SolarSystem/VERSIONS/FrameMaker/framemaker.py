import numpy as np
import matplotlib.pyplot as plt

number_of_frames = 365

framenumber = 0
while(framenumber <= number_of_frames):

    datafile = "day" + str(framenumber) + ".txt"
    positions_x, positions_y, positions_z = np.loadtxt(datafile, unpack = True)

    number_of_objects = len(positions_x)

    background_x = np.linspace(-2, 2, 100)
    background_y = np.linspace(-2, 2, 100)

    plt.figure(1, figsize = (6,4) )
    plt.xlim(-2.5, 2.5)
    plt.ylim(-2.5, 2.5)
    plt.xlabel('Position in X')
    plt.ylabel('Position in Y')

    plt.plot(positions_x, positions_y, 'bo', markersize = 1.5)
    
    framename = "frame" + str(framenumber) + ".jpg"
    plt.savefig(framename)

    framenumber = framenumber + 1

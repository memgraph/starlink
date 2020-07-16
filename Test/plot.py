import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#Function that plots 3D Earth projection

earth_radius = 6378.0 #km

def plot():
    fig = plt.figure(figsize=(18,6))
    ax = fig.add_subplot(111, projection='3d')

    #plot trajectories
    #here goes the orbits we need to calculate

    #plot central body, Earth in our case
    _u, _v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    _x = earth_radius * np.cos(_u) * np.sin(_v)
    _y = earth_radius * np.sin(_u) * np.sin(_v)
    _z = earth_radius * np.cos(_v)
    ax.plot_surface(_x, _y, _z, cmap='Blues')

    ax.set_xlim([-10000, 10000])
    ax.set_ylim([-10000, 10000])
    ax.set_zlim([-10000, 10000])
    
    ax.set_xlabel([' X (km) '])
    ax.set_ylabel([' Y (km) '])
    ax.set_zlabel([' Z (km) '])

    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot()
    

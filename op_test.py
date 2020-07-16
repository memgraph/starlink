import numpy as np
import planetary_data as  pd
import tools as  t
import matplotlib.pyplot as plt
from math import sqrt
from scipy.integrate import ode
from mpl_toolkits.mplot3d import Axes3D
from OrbitPropagator import OrbitPropagator as  OP

plt.style.use('dark_background')

cb=pd.earth         # constants for the central body
tspan = 3600*24*1.0 # timepsan
dt=10.0             # time interval for calculation

if __name__ == '__main__':
    
    objects = t.tle2coes1file('objects.txt')       # read the TLE set
    ops = []
    for o in objects:
        op=OP(o,tspan,dt,coes=True,deg=False)       # create on OrbitPropagator instance for every object
        op.propagate_orbit()                        # calculate the orbit for every object
        ops.append(op.rs)

    t.plot_n_orbits(ops, labels=[], show_plot=True) # plot all the orbits of all the objects

    """
    op0=OP(t.tle2coes('iss.txt'),tspan,dt,coes=True,deg=False)
    op1=OP(t.tle2coes('cosmos.txt'),tspan,dt,coes=True,deg=False)
    op2=OP(t.tle2coes('progress.txt'),tspan,dt,coes=True,deg=False)
    op0.propagate_orbit()
    op1.propagate_orbit()
    op2.propagate_orbit()
    t.plot_n_orbits([op0.rs, op1.rs, op2.rs], labels=['ISS','COSMOS','PROGRESS'], show_plot=True)
    """
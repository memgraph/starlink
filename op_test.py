import planetary_data as pd
import tools as t
import matplotlib.pyplot as plt
from OrbitPropagator import OrbitPropagator as OP

plt.style.use('dark_background')

cb = pd.earth         # constants for the central body
tspan = 3600*24*1.0  # timepsan (24 hours in seconds)
dt = 1800.0            # time interval for calculation (1 hour in seconds)

if __name__ == '__main__':

    ax = t.plot_central_body(cb)

    objects = t.tle2coes1file('objects.txt')       # read the TLE set

    rss = []
    for o in objects:
        op = OP(o, tspan, dt, coes=True, deg=False)
        op.propagate_orbit()                        # calculate the orbit for every object
        rss.append(op.rs)

    # plot all the orbits of all the objects
    t.plot_orbits(ax, rss, show_plot=True, title='Orbit Simulator')
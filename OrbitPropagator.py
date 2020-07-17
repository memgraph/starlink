import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from mpl_toolkits.mplot3d import Axes3D
import planetary_data as pd
import tools as t


class OrbitPropagator:
    def __init__(self, state0, tspan, dt, coes=False, deg=True, cb=pd.earth):
        if coes:
            self.r0, self.v0 = t.coes2rv(state0, deg=deg, mu=cb['mu'])
        else:
            self.r0 = state0[:3]
            self.v0 = state0[3:]
        self.y0 = self.r0.tolist()+self.v0.tolist()
        self.tspan = tspan
        self.dt = dt
        self.cb = cb

        # total number of steps
        self.n_steps = int(np.ceil(self.tspan/self.dt))

        # initialize arrays
        self.ys = np.zeros((self.n_steps, 6))
        self.ts = np.zeros((self.n_steps, 1))

        # initial conditions

        self.ys[0, :] = self.y0
        self.ts[0] = 0
        self.step = 1

        # initiate solver
        self.solver = ode(self.diffy_q)
        self.solver.set_integrator('dopri5')
        self.solver.set_initial_value(self.y0, 0)

    def propagate_orbit(self):
        # propagate orbit
        while self.solver.successful() and self.step < self.n_steps:
            self.solver.integrate(self.solver.t + self.dt)
            self.ts[self.step] = self.solver.t
            self.ys[self.step] = self.solver.y
            self.step += 1

        self.rs = self.ys[:, :3]
        self.vs = self.ys[:, 3:]

    def diffy_q(self, t, y):
        rx, ry, rz, vx, vy, vz = y
        r = np.array([rx, ry, rz])
        v = np.array([vx, vy, vz])

        norm_r = np.linalg.norm(r)

        ax, ay, az = -r*self.cb['mu']/(norm_r**3)

        return [vx, vy, vz, ax, ay, az]

    def plot_3d(self, show_plot=False, save_plot=False, title='Test Title'):
        # 3D plot
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(111, projection='3d')

        # plot trajectory and starting point
        ax.plot(self.rs[:, 0], self.rs[:, 1],
                self.rs[:, 2], 'w', label='Trajectory')
        ax.plot([self.rs[0, 0]], [self.rs[0, 1]], [
                self.rs[0, 2]], 'wo', label='Initial Position')

        # plot central body
        r_plot = self.cb['radius']
        _u, _v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        _x = r_plot*np.cos(_u)*np.sin(_v)
        _y = r_plot*np.sin(_u)*np.sin(_v)
        _z = r_plot*np.cos(_v)
        ax.plot_surface(_x, _y, _z, cmap='Blues')

        # plot the x,y,z vectors
        l = r_plot*2.0
        x, y, z = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        u, v, w = [[l, 0, 0], [0, l, 0], [0, 0, l]]
        ax.quiver(x, y, z, u, v, w, color='k')

        # check for custom axes limits
        max_val = np.max(np.abs(self.rs))

        # set labels and title
        ax.set_xlim([-max_val, max_val])
        ax.set_ylim([-max_val, max_val])
        ax.set_zlim([-max_val, max_val])

        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')

        ax.set_title(title)
        plt.legend()

        if show_plot:
            plt.show()
        if save_plot:
            plt.savefig(title+'.png', dpi=300)

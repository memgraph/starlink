import numpy as np
import math as m
import matplotlib.pyplot as plt
import planetary_data as pd
import datetime
from mpl_toolkits.mplot3d import Axes3D

d2r = np.pi/180.0

# plot the central body (earth)

def plot_central_body(cb=pd.earth):
    # 3D plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    r_plot = cb['radius']
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
    max_val = r_plot+1500.0

    # set labels
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])

    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    return ax

# plot the trajectories of the objects (satellites)

def plot_orbits(ax, rs, show_plot=False, save_plot=False, title=''):
    for r in rs:
        ax.scatter(r[:, 0], r[:, 1], r[:, 2], 'w')
    
    ax.set_title(title)

    if show_plot:
        plt.show()
    if save_plot:
        plt.savefig(title+'.png', dpi=300)

# plot the central body and all the orbits

def plot_central_body__and_orbits(rs, labels, cb=pd.earth, show_plot=False, save_plot=False, title=''):

    # 3D plot
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')

    # plot trajectory and starting point
    n = 0
    for r in rs:
        # ax.plot(r[:, 0], r[:,1], r[:,2], 'w', label=labels[n])     # labels can be used only if there are a few satellites
        ax.scatter(r[:, 0], r[:, 1], r[:, 2], 'wo')
        # ax.plot([r[0,0]], [r[0,1]], [r[0,2]], 'wo')                # starting point
        n += 1

    # plot central body
    r_plot = cb['radius']
    _u, _v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    _x = r_plot*np.cos(_u)*np.sin(_v)
    _y = r_plot*np.sin(_u)*np.sin(_v)
    _z = r_plot*np.cos(_v)
    ax.plot_surface(_x, _y, _z, cmap='Blues')

    # plot the x,y,z vectors for orientation purposes
    l = r_plot*2.0
    x, y, z = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    u, v, w = [[l, 0, 0], [0, l, 0], [0, 0, l]]
    ax.quiver(x, y, z, u, v, w, color='k')

    # check for custom axes limits
    max_val = np.max(np.abs(rs))

    # set labels and title
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])

    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    ax.set_title(title)
    # plt.legend()

    if show_plot:
        plt.show()
    if save_plot:
        plt.savefig(title+'.png', dpi=300)


def coes2rv(coes, deg=False, mu=pd.earth['mu']):
    if deg:
        a, e, i, ta, aop, raan = coes
        i *= d2r
        ta *= d2r
        aop *= d2r
        raan *= d2r
    else:
        a, e, i, ta, aop, raan, date = coes
    E = ecc_anomaly([ta, e], 'tae')
    r_norm = a*(1-e**2)/(1+e*np.cos(ta))
    r_perif = r_norm * np.array([m.cos(ta), m.sin(ta), 0])
    v_perif = m.sqrt(mu*a)/r_norm * \
        np.array([-m.sin(E), m.cos(E)*m.sqrt(1-e**2), 0])

    perif2eci = np.transpose(eci2perif(raan, aop, i))

    r = np.dot(perif2eci, r_perif)
    v = np.dot(perif2eci, v_perif)

    return r, v


def eci2perif(raan, aop, i):
    row0 = [-m.sin(raan)*m.cos(i)*m.sin(aop)+m.cos(raan)*m.cos(aop), m.cos(raan)
            * m.cos(i)*m.sin(aop)+m.sin(raan)*m.cos(aop), m.sin(i)*m.sin(aop)]
    row1 = [-m.sin(raan)*m.cos(i)*m.cos(aop)-m.cos(raan)*m.sin(aop), m.cos(raan)
            * m.cos(i)*m.cos(aop)-m.sin(raan)*m.sin(aop), m.sin(i)*m.cos(aop)]
    row2 = [m.sin(raan)*m.sin(i), -m.cos(raan)*m.sin(i), m.cos(i)]
    return np.array([row0, row1, row2])


def ecc_anomaly(arr, method, tol=1e-8):
    if method == 'newton':
        Me, e = arr
        if Me < np.pi/2.0:
            E0 = Me+e/2.0
        else:
            E0 = Me-e
        for n in range(200):
            ratio = (E0-e*np.sin(E0)-Me)/(1-e*np.cos(E0))
            if abs(ratio) < tol:
                if n == 0:
                    return E0
                else:
                    return E1
            else:
                E1 = E0-ratio
                E0 = E1
        return False
    elif method == 'tae':
        ta, e = arr
        return 2*m.atan(m.sqrt((1-e)/(1+e))*m.tan(ta/2.0))
    else:
        print('Must enter method')


def tle2coes1file(tle_filename, mu=pd.earth['mu']):
    with open(tle_filename, 'r') as f:
        lines = f.readlines()
    cnt = 0
    objects = []
    while(cnt < len(lines)):
        line0 = lines[cnt].strip()
        line1 = lines[cnt+1].strip().split()
        line2 = lines[cnt+2].strip().split()

        epoch = line1[3]
        year, month, day, hour = calc_epoch(epoch)

        i = float(line2[2])*d2r
        raan = float(line2[3])*d2r
        e_string = line2[4]
        e = float('0.'+e_string)
        aop = float(line2[5])*d2r
        Me = float(line2[6])*d2r
        mean_motion = float(line2[7])
        T = 1/mean_motion*24*3600
        a = (T**2*mu/4.0/np.pi**2)**(1/3.0)

        F = ecc_anomaly([Me, e], 'newton')
        ta = true_anomaly([F, e])
        r_mag = a*(1-e*np.cos(F))

        objects.append([a, e, i, ta, aop, raan, [year, month, day, hour]])
        cnt += 3
    return objects


def tle2coes(tle_filename, mu=pd.earth['mu']):
    with open(tle_filename, 'r') as f:
        lines = f.readlines()

    line0 = lines[0].strip()
    line1 = lines[1].strip().split()
    line2 = lines[2].strip().split()

    epoch = line1[3]
    year, month, day, hour = calc_epoch(epoch)

    i = float(line2[2])*d2r
    raan = float(line2[3])*d2r
    e_string = line2[4]
    e = float('0.'+e_string)
    aop = float(line2[5])*d2r
    Me = float(line2[6])*d2r
    mean_motion = float(line2[7])
    T = 1/mean_motion*24*3600
    a = (T**2*mu/4.0/np.pi**2)**(1/3.0)

    F = ecc_anomaly([Me, e], 'newton')
    ta = true_anomaly([F, e])
    r_mag = a*(1-e*np.cos(F))

    return a, e, i, ta, aop, raan, [year, month, day, hour]


def calc_epoch(epoch):
    year = int('20'+epoch[:2])

    epoch = epoch[2:].split('.')

    day_of_year = int(epoch[0])-1

    hour = float('0.'+epoch[1])*24.0

    date = datetime.date(year, 1, 1)+datetime.timedelta(day_of_year)
    month = float(date.month)
    day = float(date.day)
    return year, month, day, hour


def true_anomaly(arr):
    E, e = arr
    return 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(E/2.0))


def tle2rv(tle_filename):
    return coes2rv(tle2coes(tle_filename))

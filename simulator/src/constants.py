SIZE_X = 360    # degrees [-180,180]
SIZE_Y = 180    # degrees [-90,90]
SAT_ALT = 550   # KM
NUM_ORB = 24    # number of orbits for Starlink Phase 1 (FCC filing Nov 2018)
NUM_OBJ = 33    # number of satellites per orbits for Starlink Phase 1 (FCC filing Nov 2018)

"""Starlink constellation: 24 orbits, 33 satellites per orbit, orbital shell inclination of 63 degrees, altitude of 550 km"""
TLE_FILE = "imports/tle_1"

"""Starlink constellation: 24 orbits, 10 satellites per orbit, orbital shell inclination of 63 degrees, altitude of 550 km"""
#TLE_FILE = "imports/tle_2"

"""Starlink constellation: 24 orbits, 20 satellites per orbit, orbital shell inclination of 63 degrees, altitude of 550 km"""
#TLE_FILE = "imports/tle_3"

V_LASER_VACUUM = 2.99792458E+8
V_LASER_CABLE = 2.04190477E+8
V_RADIO = 2.99792458E+8
SAT_DELAY = 0.004   # ms
RELAY_DELAY = 0.008   # ms
VIEW_ANGLE = 70
CITIES_FILE = "imports/cities.csv"
EDGE_CONNECTED = True
DB_UPDATE_TIME = 0 
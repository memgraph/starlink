from starlink_simulator.stationary_object import StationaryObject as StationaryObject
import starlink_simulator.utils as utils

class City(StationaryObject):
    def __init__(self, id, x, y, z, name):
        StationaryObject.__init__(self, id, x, y, z)
        self.name = name
        self.id = id
        
        #city loaction
        self.x = x
        self.y = y
        self.z = z

        self.moving_objects_distances_dict = {}

    #Calculate distances between cities and all moving objects 
    def calc_dist_cities_and_moving_objects_All(self, all_moving_objects):
        for moving_object in all_moving_objects:    
            dist = utils.distance3D(self, moving_object)
            self.moving_objects_distances_dict[moving_object.id] = dist

    #Calculates distances between cities and moving objects in 45° field of view
    def calc_dist_cities_and_moving_objects_45(self, all_moving_objects):
        for moving_object in all_moving_objects
            angle = utils.calculate_angle(self, moving_object)
            #[67, 135]
            if angle >= 45 and angle <= 135:
                dist = utils.distance3D(city, moving_object)
                self.moving_objects_distances_dict[moving_object.id] = dist

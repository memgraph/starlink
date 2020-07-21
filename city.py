from stationary_object import StationaryObject as StationaryObject

class City(StationaryObject):
    def __init__(self, id, x, y, z, name):
        StationaryObject.__init__(self, id, x, y, z)
        self.name = name

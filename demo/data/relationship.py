
class Relationship():
    def __init__(self, xS, yS, zS, xE, yE, zE, connection, transmission_time):
        #start of connection
        self.xS = xS
        self.yS = yS
        self.zS = zS

        #end of connection
        self.xE = xE
        self.yE = yE
        self.zE = zE

        #is connection on or off?
        self.connection = connection

        #transmission time in between starting and ending point
        self.transmission_time = transmission_time
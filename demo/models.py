from django.db import models

# Create your models here.

class Satellite(models.Model):
    satellite_id = models.IntegerField
    satellite_id_in_orbit = models.IntegerField
    orbit_id = models.IntegerField
    is_in_horizontal_orbit = model.BooleanField

    #Initial coordinates
    x0 = model.FloatField
    y0 = model.FloatField
    z0 = model.FloatField

    #Current position in the orbit
    x = x0
    y = y0
    z = z0

    #Laser connections
    laser_left_id = model.IntegerField
    laser_left_id_in_orbit = model.IntegerField
    laser_right_id= model.IntegerField
    laser_right_id_in_orbit = model.IntegerField

class City(models.Model):
    city_id = models.IntegerField
    city_name = models.CharField(max_length = 50)

    #city coordinates
    x = model.FloatField
    y = model.FloatField
    z = model.FloatField

    #moving_objects_dist_dict ???

class Connection(models.Model):




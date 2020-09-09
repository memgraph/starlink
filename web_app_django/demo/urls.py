from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check', views.check, name='check'),
    path('post/ajax/json_satellites_and_relationships', views.postSatellitesAndRelationships, name = "json_satellites_and_relationships"),
]
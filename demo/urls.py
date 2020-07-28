from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/ajax/json_satellites', views.postSatellites, name = "json_satellites"),
]
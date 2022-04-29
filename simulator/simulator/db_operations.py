import logging
from typing import List, Dict, Any
import json
from time import sleep

logger = logging.getLogger('simulator')


def create_data(producer: Any,
                moving_objects_dict_by_id: Any,
                cities: Any) -> None:

    logger.info(f'Creating initial data')

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        satellite_message = {
            'id': moving_object.id,
            'x': moving_object.x,
            'y': moving_object.y,
            'z': moving_object.z}
        producer.send('satellite', json.dumps(
            satellite_message).encode('utf8'))

    for city in cities:
        city_message = {
            'id': city.id,
            'name': city.name,
            'x': city.x,
            'y': city.y}
        producer.send('city', json.dumps(city_message).encode('utf8'))
        logger.info(f'City: {city_message}')

    for city in cities:
        for key in city.moving_objects_tt_dict:
            visible_from_message = {
                'city_id': city.id,
                'satellite_id': key,
                'transmission_time': city.moving_objects_tt_dict[key]}
            producer.send('visible_from', json.dumps(
                visible_from_message).encode('utf8'))

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_left_id,
            'laser_transmission_time': moving_object.laser_left_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_right_id,
            'laser_transmission_time': moving_object.laser_right_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_up_id,
            'laser_transmission_time': moving_object.laser_up_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_down_id,
            'laser_transmission_time': moving_object.laser_down_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))


def update_data(producer: Any,
                moving_objects_dict_by_id: Any,
                cities: Any) -> None:

    logger.info(f'Updating data')

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        satellite_message = {
            'id': moving_object.id,
            'x': moving_object.x,
            'y': moving_object.y,
            'z': moving_object.z}
        producer.send('satellite', json.dumps(
            satellite_message).encode('utf8'))
            
    for city in cities:
        delete_visible_from_message = {
            'id': city.id}
        producer.send('delete_visible_from', json.dumps(
            delete_visible_from_message).encode('utf8'))

    for city in cities:
        for key in city.moving_objects_tt_dict:
            visible_from_message = {
                'city_id': city.id,
                'satellite_id': key,
                'transmission_time': city.moving_objects_tt_dict[key]}
            producer.send('visible_from', json.dumps(
                visible_from_message).encode('utf8'))

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_left_id,
            'laser_transmission_time': moving_object.laser_left_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_right_id,
            'laser_transmission_time': moving_object.laser_right_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_up_id,
            'laser_transmission_time': moving_object.laser_up_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))

        message = {
            'laser_id': moving_object.id,
            'moving_object_id': moving_object.laser_down_id,
            'laser_transmission_time': moving_object.laser_down_transmission_time}
        producer.send('laser_link', json.dumps(message).encode('utf8'))

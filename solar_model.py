# coding: utf-8
# license: GPLv3
import math
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import root_scalar
import pandas

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""

accuracy = 0.0001

maximum_iterations = 1000000

number_of_time_intervals = 1

def calculate_acceleration(stars_position, stars_mass, object_position):
    """Вычисляет ускорение тела, под действием звезд.
    """
    distances_vector = stars_position - object_position
    distances = np.linalg.norm(distances_vector, axis=1)

    abs_accelerations = stars_mass * gravitational_constant / distances**3

    accelerations = distances_vector * abs_accelerations[:, np.newaxis]
    acceleration = accelerations.sum(axis=0)
    
    #print(acceleration)
    return acceleration

def find_derivative_of_acceleration(stars_position, planets_position, stars_acceleration, planets_acceleration, stars_speed, planets_speed, time, stars_mass):
    stars_derivative_of_acceleration = np.zeros((len(stars_position),2))
    planets_derivative_of_acceleration = np.zeros((len(planets_position),2))

    stars_derivative_change = np.zeros((len(stars_position)))
    planets_derivative_change = np.zeros((len(planets_position)))

    stars_acceleration_new = np.zeros((len(stars_position),2))
    planets_acceleration_new = np.zeros((len(planets_position),2))

    for i in range(maximum_iterations):
        planets_position_new, stars_position_new = move_the_world(time, stars_position, stars_acceleration, stars_speed, planets_position, planets_acceleration, planets_speed, stars_derivative_of_acceleration, planets_derivative_of_acceleration)

        for i in range(len(stars_position)):
            stars_acceleration_new[i] = calculate_acceleration(np.delete(stars_position_new, i, axis=0), np.delete(stars_mass, i, axis=0), stars_position_new[i])
        for i in range(len(planets_position)):
            planets_acceleration_new[i] = calculate_acceleration(stars_position_new, stars_mass, planets_position_new[i])

        stars_derivative_of_acceleration_last = stars_derivative_of_acceleration
        planets_derivative_of_acceleration_last = planets_derivative_of_acceleration
        stars_derivative_of_acceleration = (stars_acceleration_new - stars_acceleration) / time
        planets_derivative_of_acceleration = (planets_acceleration_new - planets_acceleration) / time

        stars_derivative_change = np.linalg.norm(stars_derivative_of_acceleration - stars_derivative_of_acceleration_last, axis=1)
        planets_derivative_change = np.linalg.norm(planets_derivative_of_acceleration - planets_derivative_of_acceleration_last, axis=1)
        
        #print(stars_derivative_change , np.linalg.norm(stars_derivative_of_acceleration, axis=1), planets_derivative_change , np.linalg.norm(planets_derivative_of_acceleration, axis=1))
        if len(stars_position) > 1 and len(planets_position) > 0 and max((stars_derivative_change / np.linalg.norm(stars_derivative_of_acceleration, axis=1)).max(), (planets_derivative_change / np.linalg.norm(planets_derivative_of_acceleration, axis=1)).max()) < accuracy:
            break
        elif len(planets_position) == 0 and (stars_derivative_change / np.linalg.norm(stars_derivative_of_acceleration, axis=1)).max() < accuracy:
            break
        elif len(stars_position) == 1 and (planets_derivative_change / np.linalg.norm(planets_derivative_of_acceleration, axis=1)).max() < accuracy:
            break

    return change_the_world(time, stars_position, stars_acceleration, stars_speed, planets_position, planets_acceleration, planets_speed, stars_derivative_of_acceleration, planets_derivative_of_acceleration)
    
    
    
def change_the_world(time, stars_position, stars_acceleration, stars_speed, planets_position, planets_acceleration, planets_speed, stars_derivative_of_acceleration, planets_derivative_of_acceleration):
    planets_position, stars_position = move_the_world(time, stars_position, stars_acceleration, stars_speed, planets_position, planets_acceleration, planets_speed, stars_derivative_of_acceleration, planets_derivative_of_acceleration)
    
    planets_speed = planets_speed + planets_acceleration*time + (planets_derivative_of_acceleration*time**2)/2
    stars_speed = stars_speed + stars_acceleration*time + (stars_derivative_of_acceleration*time**2)/2

    return planets_position, stars_position, planets_speed, stars_speed
    

def move_the_world(time, stars_position, stars_acceleration, stars_speed, planets_position, planets_acceleration, planets_speed, stars_derivative_of_acceleration, planets_derivative_of_acceleration):
    #print(planets_position, planets_acceleration, planets_speed, planets_derivative_of_acceleration)
    planets_position = planets_position + planets_speed*time + (planets_acceleration*time**2)/2 + (planets_derivative_of_acceleration*time**3)/6
    stars_position = stars_position + stars_speed*time + (stars_acceleration*time**2)/2 + (stars_derivative_of_acceleration*time**3)/6

    return planets_position, stars_position

def move_space_objects(total_time, stars, planets):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    stars_speed = np.zeros((len(stars),2))
    stars_position = np.zeros((len(stars),2))
    for i in range(len(stars)):
        stars_speed[i] = np.array([stars[i].Vx, stars[i].Vy])
        stars_position[i] = np.array([stars[i].x, stars[i].y])

    stars_mass = np.array([body.m for body in stars])

    planets_speed = np.zeros((len(planets),2))
    planets_position = np.zeros((len(planets),2))
    for i in range(len(planets)):
        planets_speed[i] = np.array([planets[i].Vx, planets[i].Vy])
        planets_position[i] = np.array([planets[i].x, planets[i].y])

    stars_acceleration = np.zeros((len(stars_position),2))
    planets_acceleration = np.zeros((len(planets_position),2))

    for i in range(len(stars_position)):
        stars_acceleration[i] = calculate_acceleration(np.delete(stars_position, i, axis=0), np.delete(stars_mass, i, axis=0), stars_position[i])
    for i in range(len(planets_position)):
        planets_acceleration[i] = calculate_acceleration(stars_position, stars_mass, planets_position[i])
    
    minimal_time = total_time / number_of_time_intervals  

    while total_time>0:
        time = min(total_time, minimal_time)   
        total_time -= time    
    
        planets_position, stars_position, planets_speed, stars_speed = find_derivative_of_acceleration(stars_position, planets_position, stars_acceleration, planets_acceleration, stars_speed, planets_speed, time, stars_mass)

    for i in range(len(stars)):
        stars[i].Vx,stars[i].Vy = stars_speed[i]
        stars[i].x,stars[i].y = stars_position[i]
    for i in range(len(planets)):
        planets[i].Vx,planets[i].Vy = planets_speed[i]
        planets[i].x,planets[i].y = planets_position[i]


def recalculate_space_objects_positions(space_objects, time):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    
    if len(space_objects)>0:
        stars=[]
        planets=[]
        for obj in space_objects:
            if obj.type=='star':
                stars.append(obj)
            elif obj.type=='planet':
                planets.append(obj)
        move_space_objects(time, stars, planets)   

if __name__ == "__main__":
    print("This module is not for direct call!")

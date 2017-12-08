"""
General utilities - these have no dependency on Panther itself
"""
import math


def move_on_angle(angle, curr_x, curr_y, to_move):
    """
    Calculates the new x, y loc of something which has been translated <to_move> distance at <angle>
    :param angle: int, 0 <= angle < 360. angle == 90 means right
    :param curr_x: number, current x location
    :param curr_y: number, current y location
    :param to_move: number, distance to move at this angle
    :return: tuple<x(int), y(int)>, new x and y co-ordinates
    """
    angle = math.radians(angle + 90)  # convert to radians, and set 0 to mean right, instead of 90

    x_to_move = math.cos(angle) * to_move
    y_to_move = math.sin(angle) * to_move

    return math.floor(x_to_move + curr_x), math.floor(y_to_move + curr_y)

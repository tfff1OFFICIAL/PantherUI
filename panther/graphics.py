"""
Graphics part, this communicates with the panther.canvas through a nice little API
"""
from kivy.graphics import *
import panther
from panther.util import hex_to_rgb
#from panther import Drawable, DrawableGroup


def _draw_graphic(obj):
    """
    adds a kivy.graphics object to the panther._draw_queue
    :param obj: kivy.graphics object
    :return: None
    """
    #panther._draw_queue.put(obj)
    try:
        panther.canvas.canvas.add(obj)
    except AttributeError:
        raise Exception("You may only call graphics functions from within the draw event")


def clear():
    """
    clear the screen
    :return: None
    """
    panther.canvas.clear()


def set_colour(colour):
    """
    Set the colour of whatever is painted next
    :param rgb: tuple<red(int), green(int), blue(int)>
    :param hex: string
    :return: None
    """
    if isinstance(colour, tuple) or isinstance(colour, list):
        _draw_graphic(Color(*colour))
    elif isinstance(colour, str) and len(colour) == 6:
        _draw_graphic(Color(*hex_to_rgb(colour)))
    else:
        print(colour)
        raise ValueError("valid hex or rgb value must be present")


def set_background_color(colour):
    """
    sets the background colour of the screen
    :param rgb: tuple<red(int), green(int), blue(int)>
    :return: None
    """
    set_colour(colour)
    _draw_graphic(Rectangle(size=panther.canvas.size, pos=panther.canvas.pos))


def ellipse(x, y, size_x, size_y):
    """
    draw an ellipse
    :param x: int, x co-ord
    :param y: int, y co-ord
    :param size_x: int, size on the x axis
    :param size_y: int, size on the y axis
    :return: None
    """
    _draw_graphic(Ellipse(
        pos=(x - size_x / 2, y - size_y / 2),
        size=(size_x, size_y)
    ))


def circle(x, y, radius):
    """
    draw a circle
    :param x: int, x co-ord
    :param y: int, y co-ord
    :param radius: int, radius of circle
    :return: None
    """
    _draw_graphic(Ellipse(
        pos=(x-radius, y-radius),
        size=(radius*2, radius*2)
    ))
"""
Graphics part, this communicates with the panther.canvas through a nice little API
"""
from math import pi, sin, cos
from kivy.graphics import *
from kivy.core.image import Image as CoreImage
import panther
from panther.util import hex_to_rgb


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


def rectangle(x, y, width, height):
    """
    creates a new rectangle
    :param x: int, x co-ord
    :param y: int, y co-ord
    :param width: int, width
    :param height: int, height
    :return: None
    """
    _draw_graphic(Rectangle(
        pos=(x, y),
        size=(width, height)
    ))


def triangle(x, y):
    """
    creates a new triangle
    :param x: int, x co-ord
    :param y: int, y co-ord
    :return: None
    """
    raise NotImplementedError()


def regular_polygon(radius, sides, x, y):
    r = radius
    a = 2 * pi / sides
    vertices=[]
    for i in range(sides):
        vertices += [
            x + cos(i * a) * r,
            y + sin(i * a) * r,
            cos(i * a),
            sin(i * a),
        ]
    _draw_graphic(Mesh(
        vertices=vertices,
        indices=len(range(sides)),
        mode='triangle_fan'
    ))


def polygon(*points):
    """
    Create a filled polygon with sides at each of the co-ordinates
    :param points: tuple<tuple<int(x), int(y)> >, each of the points in the polygon (in order)
    :return: None
    """
    p = []
    for point in points:
        p.append(point[0])
        p.append(point[1])
    _draw_graphic(Mesh(
        vertices=p,
        indices=list(range(len(p))),
        mode="triangle_fan"
    ))


def ellipse(x, y, size_x, size_y, angle_start=0, angle_end=360):
    """
    draw an ellipse
    :param x: int, x co-ord
    :param y: int, y co-ord
    :param size_x: int, size on the x axis
    :param size_y: int, size on the y axis
    :param angle_start: int, angle to start drawing ellipse
    :param angle_end: int, angle to end drawing ellipse
    :return: None
    """
    _draw_graphic(Ellipse(
        pos=(x - size_x / 2, y - size_y / 2),
        size=(size_x, size_y)
    ))


def circle(x, y, radius,angle_start=0, angle_end=360):
    """
    draw a circle
    :param x: int, x co-ord
    :param y: int, y co-ord
    :param radius: int, radius of circle
    :return: None
    """
    ellipse(x, y, radius * 2, radius * 2, angle_start, angle_end)


def line(*args, **kwargs):
    _draw_graphic(Line(*args, **kwargs))


def image(x, y, height, width, src):
    """
    draw image at <src>
    :param x: int, x co-ord
    :param y: int, y co-ord
    :param height: int, height
    :param width: int, width
    :param src: string, location of image to load
    :return: None
    """
    im = CoreImage(src)
    #print(im.texture)

    _draw_graphic(Rectangle(
        texture=im.texture,
        pos=(x, y),
        size=(width, height)
    ))


def tiling_image(x, y, width, height, src):
    raise NotImplementedError()
    Color(.4, .4, .4, 1)
    texture = CoreImage(src).texture
    texture.wrap = 'repeat'
    #print(f"width: {texture.width}, height: {texture.height}")

    nx = float(width) / texture.width
    ny = float(height) / texture.height
    Rectangle(pos=(x, y), size=(width, height), texture=texture,
              tex_coords=(0, 0, nx, 0, nx, ny, 0, ny))
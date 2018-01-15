from math import pi, sin, cos
from kivy.graphics import *
from kivy.utils import get_color_from_hex
from kivy.core.image import Image as CoreImage
from kivy.core.text import Label as CoreLabel
import panther
from panther.util import hex_to_rgb


class TextStyle:
    def __init__(
            self,
            font_size=12,
            font_name="panther/font/Roboto-Regular.ttf",
            bold=False,
            italic=False,
            underline=False,
            strikethrough=False,
            halign='left',
            valign='bottom',
            shorten=False,
            text_size=None,
            mipmap=False,
            color=None,
            line_height=1.0,
            strip=False,
            strip_reflow=True,
            shorten_from='center',
            split_str=' ',
            unicode_errors='replace',
            font_hinting='normal',
            font_kerning=True,
            font_blended=True,
            outline_width=None,
            outline_color=None
    ):
        self.font_size = font_size
        self.font_name = font_name
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
        self.halign = halign
        self.valign = valign
        self.shorten = shorten
        self.text_size = text_size
        self.mipmap = mipmap
        self.color = color
        self.line_height = line_height
        self.strip = strip
        self.strip_reflow = strip_reflow
        self.shorten_from = shorten_from
        self.split_str = split_str
        self.unicode_errors = unicode_errors
        self.font_hinting = font_hinting
        self.font_kerning = font_kerning
        self.font_blended = font_blended
        self.outline_width = outline_width
        self.outline_color = outline_color

    @property
    def style(self):
        return self.__dict__


class GraphicsManager:
    """
    instead of the extra file, each layer will have it's own one of these which it can use to draw graphics. This is to be passed to the draw function
    """

    def __init__(self, layer):
        self.layer = layer

    def _draw_graphic(self, obj):
        """
        adds a kivy.graphics object to the panther._draw_queue
        :param obj: kivy.graphics object
        :return: None
        """
        try:
            self.layer.widget.canvas.add(obj)
        except AttributeError as ex:
            print(ex)
            raise Exception("You may only call graphics functions from within the draw event handler")

    def clear(self):
        """
        clear the screen
        :return: None
        """
        self.layer.canvas.clear()

    def rotate(self, x_origin, y_origin, degrees):
        """
        rotate the canvas by <degrees> degrees
        :param x_origin: number, x co-ordinate to act as centre of rotation
        :param y_origin: number, y co-ordinate to act as centre of rotation
        :param degrees: number
        :return: None
        """
        self._draw_graphic(PushMatrix())
        self._draw_graphic(Rotate(
            angle=degrees,
            origin=(x_origin, y_origin)
        ))

    def unrotate(self):
        """
        resets the canvas' rotation
        :return: None
        """
        self._draw_graphic(PopMatrix())

    def set_colour(self, colour):
        """
        Set the colour of whatever is painted next
        :param rgb: tuple<red(int), green(int), blue(int)>
        :param hex: string
        :return: None
        """
        if isinstance(colour, tuple) or isinstance(colour, list):
            if len(colour) == 4:
                rgb = [colour[c] / 255 for c in range(len(colour) - 1)]

                self._draw_graphic(Color(*rgb, colour[-1]))
            elif len(colour) == 3:
                rgb = [c / 255 for c in colour]

                self._draw_graphic(Color(*rgb, 1))

        elif isinstance(colour, str) and len(colour) == 6:
            self._draw_graphic(Color(*get_color_from_hex(colour)))
        else:
            print(colour)
            raise ValueError("valid hex or rgb value must be present")

    set_color = set_colour

    def set_background_color(self, colour):
        """
        sets the background colour of the screen
        :param rgb: tuple<red(int), green(int), blue(int)>
        :return: None
        """
        self.set_colour(colour)
        self._draw_graphic(Rectangle(size=panther.canvas.size, pos=panther.canvas.pos))

    set_background_colour = set_background_color

    def rectangle(self, x, y, width, height):
        """
        creates a new rectangle, with the bottom left corner at <x>, <y>
        :param x: int, x co-ord
        :param y: int, y co-ord
        :param width: int, width
        :param height: int, height
        :return: None
        """
        self._draw_graphic(Rectangle(
            pos=(x, y),
            size=(width, height)
        ))

    def triangle(self, x, y):
        """
        creates a new triangle
        :param x: int, x co-ord
        :param y: int, y co-ord
        :return: None
        """
        raise NotImplementedError()

    def regular_polygon(self, radius, sides, x, y):
        r = radius
        a = 2 * pi / sides
        vertices = []
        for i in range(sides):
            vertices += [
                x + cos(i * a) * r,
                y + sin(i * a) * r,
                cos(i * a),
                sin(i * a),
            ]
        self._draw_graphic(Mesh(
            vertices=vertices,
            indices=list(range(sides)),
            mode='triangle_fan'
        ))

    def polygon(self, *points):
        """
        Create a filled polygon with sides at each of the co-ordinates
        :param points: tuple<tuple<int(x), int(y)> >, each of the points in the polygon (in order)
        :return: None
        """
        p = []
        a = 2 * pi / len(points) - 1
        indices = []
        for i in range(len(points)):
            p.append(points[i][0])
            p.append(points[i][1])
            p.append(points[i][0])
            p.append(points[i][1])
            indices.append(i)

        self._draw_graphic(Mesh(
            vertices=p,
            indices=indices,
            mode="triangle_fan"
        ))

    def ellipse(self, x, y, size_x, size_y, angle_start=0, angle_end=360):
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
        self._draw_graphic(Ellipse(
            pos=(x - size_x / 2, y - size_y / 2),
            size=(size_x, size_y)
        ))

    def circle(self, x, y, radius, angle_start=0, angle_end=360):
        """
        draw a circle
        :param x: int, x co-ord
        :param y: int, y co-ord
        :param radius: int, radius of circle
        :return: None
        """
        self.ellipse(x, y, radius * 2, radius * 2, angle_start, angle_end)

    def line(self, *args, **kwargs):
        self._draw_graphic(Line(*args, **kwargs))

    def image(self, x, y, height, width, src):
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
        # print(im.texture)

        self._draw_graphic(Rectangle(
            texture=im.texture,
            pos=(x, y),
            size=(width, height)
        ))

    def tiling_image(self, x, y, width, height, src):
        raise NotImplementedError()
        Color(.4, .4, .4, 1)
        texture = CoreImage(src).texture
        texture.wrap = 'repeat'
        # print(f"width: {texture.width}, height: {texture.height}")

        nx = float(width) / texture.width
        ny = float(height) / texture.height
        Rectangle(pos=(x, y), size=(width, height), texture=texture,
                  tex_coords=(0, 0, nx, 0, nx, ny, 0, ny))


    def text(self, x, y, text, style=TextStyle()):
        """
        Draw text
        :param x: int, x co-ord
        :param y: int, y co-ord
        :param text: string
        :return: None
        """
        label = CoreLabel(
            text,
            **style.style
        )

        if label.texture is None:
            label.refresh()

        # import inspect
        # import pprint
        # pprint.pprint(inspect.getmembers(label))#, lambda a: not (inspect.isroutine(a))))

        #print(label.texture)

        rect = Rectangle(
            pos=(x, y),
            texture=label.texture,
            size=(label.texture.size[0], label.texture.size[1])
        )

        #print(rect)

        self._draw_graphic(rect)

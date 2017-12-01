"""
import this to begin
"""
import time
import queue

import datetime
from . import defaults

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

'''
run = defaults.default_run
load = None  # this is called once, when the app is starting
update = None  # this is called to update every frame
draw = None  # this is called to draw stuff on the screen every frame
quit = None
'''


class EventManager:
    events = queue.Queue()

    event_handlers = dict(
        run=defaults.default_run,
        load=None,
        update=None,
        draw=None,
        quit=None
    )

    def add(self, event_name, f, **options):
        self.event_handlers[event_name] = lambda *args, **kwargs: f(*args, **kwargs)

    def trigger_event(self, event, *args, **kwargs):
        if self.event_handlers[event]:
            self.event_handlers[event](*args, **kwargs)

    # @function decorators for events
    def subscribe(self, event, **options):
        def decorator(f):
            ev = event
            self.add(event, f, **options)
            return f

        return decorator

    def __len__(self):
        return self.events.qsize()

    def __iter__(self):
        while not self.events.empty():
            yield self.events.get()


events = EventManager()


class Canvas(Gtk.DrawingArea):
    def __init__(self):
        super(Canvas, self).__init__()
        self.connect("draw", self.draw)
        self.set_size_request(800, 500)

    def draw(self, widget, event):
        """
        Draw stuff on the screen I assume?
        :param widget:
        :param event:
        :return: None
        """
        cr = widget.window.cairo_create()
        rect = self.get_allocation()

        # you can use w and h to calculate relative positions which
        # also change dynamically if window gets resized
        w = rect.width
        h = rect.height


class Conf:
    width = None
    height = None

    title = None


conf = Conf()

window = None
canvas = None


def start(width=None, height=None, title=None):
    """
    Run the panther application
    :return: None
    """
    global window, conf, events

    if width:
        conf.width = width
    if height:
        conf.height = height
    if title:
        conf.title = title

    if conf.width and conf.height and conf.title:
        window = Gtk.Window(
            title=conf.title
        )
        canvas = Canvas()

        window.add(canvas)
        #window.set_position(Gtk.gtk.WIN_POS_CENTER)
        window.show_all()

        events.trigger_event('run')
    else:
        raise ValueError("height, width, and title must be defined before start is called")


def draw_screen():
    return
    global surface, cr, conf

    if surface and cr:
        cr.fill()

        im = Image.frombuffer(
            "RGBA",
            (conf.width, conf.height),
            bytes(surface.get_data()),
            "raw",
            "BGRA",
            0,
            1
        )  # don't ask me what these are!
        im.show()


def title(t=None):
    """
    sets the title
    :param t:
    :return:
    """
    if not t:
        return


class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = time.time()

    def time(self):
        return datetime.timedelta(seconds=time.time() - self.start_time)

    def sleep(self, length):
        time.sleep(length)


timer = Timer()

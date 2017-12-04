"""
import this to begin
"""
import time
import queue
import threading
import datetime
from panther import defaults
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse

'''
run = defaults.default_run
load = None  # this is called once, when the app is starting
update = None  # this is called to update every frame
draw = None  # this is called to draw stuff on the screen every frame
quit = None
'''

'''
class Drawable:
    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        return self.obj(*self.args, **self.kwargs)

    def __repr__(self):
        return f'<Drawable (obj: {self.obj}, args: {self.args}, kwargs: {self.kwargs})>'


class DrawableGroup:
    """
    A group of drawable that MUST be drawn in the same order
    """
    def __init__(self, *objs):
        """
        :param objs: list<Drawable>
        """
        self.objs = objs

    def execute(self):
        for obj in self.objs:
            obj.execute()

    def __iter__(self):
        for obj in self.objs:
            yield obj
'''


class Event:
    def __init__(self, name, handler, args, kwargs):
        self.name = name
        self.handler = handler
        self.args = args
        self.kwargs = kwargs

    def auto_handle(self):
        """
        Just execute the handler with raw args and kwargs
        :return: any
        """
        return self.handler(*self.args, **self.kwargs)

    def __repr__(self):
        return f'<Event (name: {self.name}, handler: {self.handler.__name__}, args: {self.args}, kwargs: {self.kwargs})'


class EventManager:
    events = queue.Queue()

    event_handlers = dict(
        #run=defaults.default_run,
        load=None,
        update=None,
        draw=None,
        quit=None,
        # touch
        touchdown=lambda touch: print(f"touch: {touch} received")
    )

    def __init__(self):
        self.kivy_trigger = Clock.create_trigger(self.trigger)

    def add(self, event_name, f, **options):
        self.event_handlers[event_name] = lambda *args, **kwargs: f(*args, **kwargs)

    def trigger(self, event, *args, **kwargs):
        """
        Creates an Event to be processed later
        :param event: string
        :param args: list<any>
        :param kwargs: dict<string, any>
        :return: None
        """
        try:
            if self.event_handlers[event] is not None:  # if there's a registered event handler
                self.events.put(Event(
                    event,
                    self.event_handlers[event],
                    args,
                    kwargs
                ))
        except KeyError:
            print(f"PANTHER WARNING: {event} is not a valid event handler")

    def execute(self, event, *args, **kwargs):
        """
        executes an event right now, in the calling thread/process
        :param event: string
        :param args: list<any>
        :param kwargs: dict<string, any>
        :return: None
        """
        try:
            if self.event_handlers[event] is not None:  # if there's a registered event handler
                self.event_handlers[event](*args, **kwargs)
        except KeyError:
            print(f"PANTHER WARNING: {event} is not a valid event handler")

    # @function decorators for events
    def subscribe(self, event, **options):
        def decorator(f):
            ev = event
            self.add(event, f, **options)
            return f

        return decorator

    on = subscribe

    def __len__(self):
        return self.events.qsize()

    def __iter__(self):
        while not self.events.empty():
            yield self.events.get()


events = EventManager()


class Conf:
    width = None
    height = None

    title = None

    # protected, changes after run will have no effect
    timer = True


conf = Conf()

_window = None
canvas = None
_loop_thread = None
_draw_queue = queue.Queue()  # contains: Drawable
_canvas_create = threading.Event()


class _CanvasWidget(Widget):
    """
    This represents the Canvas, everything is drawn on it
    """
    def clear(self):
        with self.canvas:
            self.canvas.clear()

    def tick(self):
        """
        this is called every tick, clear the canvas
        :return: None
        """
        self.clear()

    def draw(self, obj, *args, **kwargs):
        """
        Draw something on the canvas
        :param obj: kivy.graphics.<something> object
        :return: None
        """
        self.canvas.add(obj)
        #with self.canvas:
        #    obj(*args, **kwargs)

    def draws(self, drawables):
        """
        Draw a lot of things on the canvas
        :param drawables: list<Drawable>
        :return: None
        """
        for item in drawables:
            self.canvas.add(item)

    def ask_to_update(self):
        self.canvas.ask_update()

    def on_touch_down(self, touch):
        global events

        #with self.canvas:
        #    Color(255,255,0)
        #    Rectangle(size=self.size, pos=self.pos)

        events.trigger("touchdown", touch)
        '''
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
        '''


class _PantherApp(App):
    """
    This is a kivy.App
    it runs in a separate Thread
    """
    def build(self):
        global canvas
        return canvas


def create_app():
    """
    this runs in a new thread
    :return: None
    """
    global canvas, _window

    print("Creating app...")

    canvas = _CanvasWidget()

    def load_event(dt):
        events.execute('load')

    def update_event(dt):
        events.execute('update', dt)
        events.execute('draw')

    Clock.schedule_once(load_event)

    update_event = Clock.schedule_interval(update_event, 1 / 30.)
    event_checker = Clock.schedule_interval(defaults.default_event_parse, 1/30.)

    _window = _PantherApp()

    _window.run()


def start(width=None, height=None, title=None):
    """
    Run the panther application
    :return: None
    """
    global _window, canvas, conf, events, _loop_thread

    if width:
        conf.width = width
    if height:
        conf.height = height
    if title:
        conf.title = title

    if conf.width and conf.height and conf.title:
        _loop_thread = threading.Thread(target=create_app)
        _loop_thread.start()

        #event = Clock.schedule_interval()

        #events.execute('run')
    else:
        raise ValueError("height, width, and title must be defined before start is called")


def draw_screen():
    global _draw_queue, canvas
    if not _draw_queue.empty():
        #print(f"_draw_queue length is: {_draw_queue.qsize()}")

        while not _draw_queue.empty():
            got = _draw_queue.get()
            #print(f"Got {got} from queue")

            canvas.draw(got)

        canvas.ask_to_update()


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


if conf.timer:
    timer = Timer()

"""
import this to begin
"""
import os
import queue
import copy
import threading
from panther import defaults
from kivy.config import Config
from kivy.clock import Clock

try:
    if os.environ['panther_dev'] == "1":
        print("PANTHER: dev mode activated!")
        #Config.set('modules', 'monitor', '')
except KeyError:
    pass


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
        load=None,  # executed when the canvas first loads
        update=None,  # executed once every tick
        draw=None,  # executed once every tick, after update
        quit=None,  # executed just before the app quits
        # pointer
        mousepos=None,

        # touch
        touchdown=None,  # executes when a touch or click event occurs
        touchup=None,  # executes when a touch or click is released
        touchdrag=None,  # executes when a drag occurs

        # keyboard
        keydown=None,
        keyup=None,

        # window
        resize=None,

        # window config
        window_config_update=defaults.default_window_config_update
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
            exe = self.event_handlers[event]
        except KeyError:
            print(f"PANTHER WARNING: {event} is not a valid event handler")
            return

        if exe is not None:  # if there's a registered event handler
            self.events.put(Event(
                event,
                self.event_handlers[event],
                args,
                kwargs
            ))

    def execute(self, event, *args, **kwargs):
        """
        executes an event right now, in the calling thread/process
        :param event: string
        :param args: list<any>
        :param kwargs: dict<string, any>
        :return: None
        """
        try:
            exe = self.event_handlers[event]
        except KeyError:
            print(f"PANTHER WARNING: {event} is not a valid event handler")
            return

        if exe is not None:  # if there's a registered event handler
            exe(*args, **kwargs)

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
    # _window bound
    width = 500
    height = 400
    title = "Panther App"

    resizable = False
    show_cursor = True

    # unchangable after start
    max_fps = 60  # maximum number of ticks (frames) per second. NOTE: this is unlikely to ever be actually hit due to slowness in the system

    # non-window-bound
    clear_every_frame = True
    differentiate_between_touches_and_clicks = False

    def __init__(self):
        #Config.set('graphics', 'width', self.width)
        #Config.set('graphics', 'height', self.height)
        #Config.set('graphics', 'resizable', self.resizable)
        events.trigger('window_config_update', key="refresh_all", value="")

    def __setattr__(self, key, value):
        '''
        if _window:  # these are window-bound, so they won't work if the window doesn't yet exist
            if key == "title":
                setattr(_window, key, value)
            elif key == "height":
                raise ValueError("Cannot modify height after calling panther.start()")
            elif key == "width":
                raise ValueError("Cannot modify width after calling panther.start()")
            elif key == "show_cursor":
                raise ValueError("Cannot modify show_cursor after calling panther.start()")
        else:
            if key in ("height", "width"):
                Config.set('graphics', key, value)
            elif key == "resizable":
                Config.set('graphics', key, value)
            elif key == "show_cursor":
                print("setting show_cursor...")
                Config.set('graphics', key, "0" if not value else "1")

            Config.write()
        '''
        if _window is not None and key == "max_fps":
            raise ValueError("Cannot modify max_fps after calling panther.start()")

        super().__setattr__(key, value)
        events.trigger('window_config_update', key=key, value=value)

    def silent_setattr(self, key, value):
        super().__setattr__(key, value)

    def parse_conf_json(self, j: dict):
        for key, value in j.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def load_from_file(self, path):
        import os, json

        if os.path.isfile(path):
            with open(path) as f:
                self.parse_conf_json(json.load(f))

    def dump_to_file(self, path):
        import json
        with open(path, 'w') as f:
            #print(f"dumping: {self.__dict__}")
            json.dump(self.__dict__, f)


class PantherLayer:
    def __init__(self):
        pass


class LayerManager:
    def __init__(self):
        self.layers = []

    def add(self):
        """
        Add a new Layer with it's own canvas
        :return: Layer
        """
        l = PantherLayer()
        self.layers.append(l)

        return l

conf = Conf()
layers = None

_window = None
canvas = None
_loop_thread = None
_draw_queue = queue.Queue()  # contains: Drawable


def create_app():
    """
    this runs in a new thread
    :return: None
    """
    global canvas, _window

    from panther._widgets import _CanvasWidget, _PantherApp

    #print("Creating app...")

    canvas = _CanvasWidget()

    def load_event(dt):
        events.execute('load')

    def update_event(dt):
        events.execute('update', dt)
        if conf.clear_every_frame:
            canvas.clear()
        events.execute('draw')

    Clock.schedule_once(load_event)

    update_event = Clock.schedule_interval(update_event, 1 / conf.max_fps)
    event_checker = Clock.schedule_interval(defaults.default_event_parse, 1/conf.max_fps)



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


def quit():
    global _window

    if _window:
        _window.stop()

    exit()

'''
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
'''
'''
# DEPRECATED: this is now done by the built-in kivy scheduler
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
'''
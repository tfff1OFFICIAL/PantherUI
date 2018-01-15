"""
Root of Panther module
"""
import threading
from collections import defaultdict
from functools import wraps
import queue
from kivy.clock import Clock
from panther import defaults
from .graphics_utils import GraphicsManager


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
    def __init__(self):
        #self.kivy_trigger = Clock.create_trigger(self.trigger)
        self.events = queue.Queue()

        self.event_handlers = dict(
            # run=defaults.default_run,
            init=None,  # executed just before the canvas loads (therefore, before first draw). Initialise local variables here, not in load
            load=None,  # executed when the canvas first loads (after first draw)
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

    def add(self, event_name, f, **options):
        self.event_handlers[event_name] = lambda *a, **kw: f(*a, **kw)

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
    def subscribe_to(self, event, **options):
        def decorator(f, *args, **kwargs):
            ev = event
            self.add(event, f, **options)
            return f

        return decorator

    on = subscribe_to

    def __len__(self):
        return self.events.qsize()

    def __iter__(self):
        while not self.events.empty():
            yield self.events.get()


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


class PantherLayerNamespace(object):
    def __init__(self):
        object.__setattr__(self, "variables", dict())

    # for cleaner use
    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, "variables")[item]
        except KeyError as ex:
            raise AttributeError(repr(item))

    def __setattr__(self, key, value):
        object.__getattribute__(self, "variables")[key] = value

    def __delattr__(self, item):
        del object.__getattribute__(self, "variables")[item]

    # for use like a dictionary
    def __getitem__(self, item):
        return self.vars[item]

    def __setitem__(self, key, value):
        self.vars[key] = value


class PantherLayer:
    """
    A canvas layer in Panther with it's own events and drawing functionality
    """
    def __init__(self, id, is_root=False):
        from panther._widgets import _CanvasWidget

        self.id = id
        self.is_root = is_root

        self.canvas = _CanvasWidget()
        self.events = EventManager()
        self.graphics = GraphicsManager(self)

        self.clear_next_frame = True

        self.namespace = PantherLayerNamespace()

    @property
    def widget(self):
        return self.canvas

    @property
    def size(self):
        return self.canvas.size

    @property
    def pos(self):
        return self.canvas.pos

    def clear_canvas(self):
        if self.clear_next_frame:
            self.canvas.clear()

    def locals(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            #return func(self.namespace, *args, **kwargs)
            return func(self.namespace, *args, **kwargs)

        return wrapped

    def parse_events(self):
        """
        load all of the events for this layer
        :return: None
        """
        for event in self.events:
            if event.name == "quit":
                print("PANTHER (layer: {}): quitting...".format(self))
                event.auto_handle()  # execute the subscriber who wants to clean up their code before we exit

                if not app_quitting:  # if for some reason only this layer is quitting, tell the rest
                    quit(calling_layer_id=id(self))

            event.auto_handle()

    def do_draw(self):
        if self.is_root:  # expose the super-simple API to the root layer
            self.events.execute("draw")
        else:
            self.events.execute("draw", graphics=self.graphics)

    def start(self):
        global _window

        if _window is not None:
            _window.add_widget(self.canvas)
        else:
            raise RuntimeError("panther._window is not defined, therefore the layer cannot be started")

        #self.events.execute("load")

    def __repr__(self):
        return f'<Layer (id: {self.id})>'

class LayerManager:
    def __init__(self):
        self.layers = []

    def add(self, name=None):
        l = PantherLayer(id=(str(len(self.layers)) if name is None else name))
        self.layers.append(l)

        if started:
            l.start()

        return l

    def add_root(self):
        l = PantherLayer(id="root", is_root=True)
        self.layers.append(l)

        return l

    def init_layers(self):
        # inits the layers _before_ they first are drawn
        for layer in self:
            layer.events.execute("init")

    def start_layers(self):
        # starts all of the layers after _window has been created
        for layer in self.layers[1:]:
            layer.start()

    def __getitem__(self, item):
        return self.layers[item]

    def __setitem__(self, key, value):
        raise Exception("You cannot replace a layer once it's been created")

    def __delitem__(self, key):
        raise Exception("You cannot delete a layer once it's been created (yet)")

    def __iter__(self):
        return iter(self.layers)


_window = None
layers = LayerManager()
started = False
app_quitting = False

# simple (root-layer) API
canvas = layers.add_root()
events = canvas.events
graphics = canvas.graphics
locals = canvas.locals


conf = Conf()


def create_app():
    """
    create the Window, and add the root canvas
    :return: None
    """
    global canvas, _window, started

    from panther._widgets import _PantherApp

    def update_event(dt):
        for layer in layers:
            layer.events.execute('update', dt)
            if conf.clear_every_frame:
                layer.clear_canvas()
            layer.do_draw()

    update_event = Clock.schedule_interval(update_event, 1 / conf.max_fps)
    event_checker = Clock.schedule_interval(defaults.default_multilayer_event_parse, 1 / conf.max_fps)

    layers.init_layers()

    _window = _PantherApp()

    layers.start_layers()

    started = True

    _window.run()


def start(width=None, height=None, title=None):
    global _window, layers, started

    if width is not None:
        conf.width = width
    if height is not None:
        conf.height = height
    if title is not None:
        conf.title = title

    if not started:
        if conf.width and conf.height and conf.title is not None:
            create_app()
    else:
        raise Exception("You cannot start panther more than once!")


def trigger_event(*args, **kwargs):
    for layer in layers:
        layer.events.trigger(*args, **kwargs)


def load():
    for layer in layers:
        layer.events.execute("load")


def quit(code=0, calling_layer_id=None):
    for layer in layers:
        if calling_layer_id and id(layer) == calling_layer_id:
            continue  # skip the calling layer (if any) because they've already quit

        layer.events.execute('quit')

    exit(code)

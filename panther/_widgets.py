from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color
import panther


class _CanvasWidget(Widget):
    """
    This represents the Canvas, everything is drawn on it
    """
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

        self.canvas.add(Color([0, 0, 0, 0]))

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        panther.trigger_event("keyup", keyboard, keycode)

        return True

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        panther.trigger_event("keydown", keyboard, keycode, text, modifiers)

        return True  # keep the app open, even if ESC is pressed

    def clear(self):
        with self.canvas:
            self.canvas.clear()

    def tick(self):
        """
        this is called every tick, clear the canvas
        :return: None
        """
        self.clear()

    def draw(self, obj):
        """
        Draw something on the canvas
        :param obj: kivy.graphics.<something> object
        :return: None
        """
        self.canvas.add(obj)

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
        panther.trigger_event("touchdown", touch)

    def on_touch_up(self, touch):
        panther.trigger_event("touchup", touch)

    def on_touch_move(self, touch):
        panther.trigger_event("touchdrag", touch)


class _PantherApp(BoxLayout, App):
    """
    This is a kivy.App
    it runs in a separate Thread
    """
    def on_stop(self):
        panther.quit()  # call quit on every layer

    def on_start(self):
        panther.load()  # call load on every layer

    def on_resize(self, window, width, height):
        # TODO: maybe modify the panther.conf here too?
        if panther.conf.resizable:  # automatically apply to config
            panther.conf.silent_setattr("width", width)
            panther.conf.silent_setattr("height", height)

        def apply_func():
            """
            this is passed to the resize event function, it calls this to apply the resize properly
            :return: None
            """
            print(f"applying width: {width}, height: {height}")
            panther.conf.silent_setattr("width", width)
            panther.conf.silent_setattr("height", height)

        panther.trigger_event('resize', width, height)#, apply_func)

    def on_mouse_pos(self, window, pos):
        panther.trigger_event('mousepos', pos)

    def apply_conf(self, key, value):
        """
        Apply config, this is called once on build, and could be called later
        :return: None
        """

        if key == "refresh_all":
            Window.show_cursor = panther.conf.show_cursor
            Window.size = (panther.conf.width, panther.conf.height)
            Window.resizable = panther.conf.resizable

        elif key == "show_cursor":
            Window.show_cursor = panther.conf.show_cursor
        elif key in ("width", "height"):
            Window.size = (panther.conf.width, panther.conf.height)
        elif key == "resizable":
            Window.resizable = panther.conf.resizable
        elif key == "title":
            self.title = panther.conf.title

    def build(self):
        Window.bind(on_resize=self.on_resize, mouse_pos=self.on_mouse_pos)
        Window.show_cursor = False

        self.title = panther.conf.title

        self.add_widget(panther.canvas.widget)

        return self

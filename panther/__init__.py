"""
Root of the Panther UI module
"""
from collections import defaultdict


class EventManager:
    def __init__(self):
        self.events = defaultdict(default_factory=lambda: lambda: None)

    def add(self, name, function):
        self.events[name] = function

    def trigger(self, name, *args, **kwargs):
        self.events[name](*args, **kwargs)


class PantherApp:
    """
    Panther App
    """
    def __init__(self, title, width, height):
        # type: (str, int, int) -> PantherApp(title, width, height)
        self.title = title
        self.width = width
        self.height = height

        self._eventmanager = EventManager()

    def add_event_handler(self, event, function, **options):
        """
        Adds an event handler
        :param event: string, name of event
        :param function: function
        :param options: dict<extra options>
        :return: None
        """
        self._eventmanager.add(event, function)

    def on(self, event, **options):
        """
        Register an event function using this as a function decorator.
        e.g:
            @on('init')
            function init():
                ...
        :param event: string, name of event
        :return:
        """

        def decorator(f):
            ev = event
            self.add_event_handler(event, f, **options)
            return f

        return decorator

    def start(self):
        """
        Runs the app
        :return: None
        """
        # start the app up

        # run init
        self._eventmanager.trigger('init')


if __name__ == "__main__":
    app = PantherApp(
        "test app",
        500,
        500
    )

    @app.on('init')
    def panther_init():
        print("initialising panther app")

    app.start()

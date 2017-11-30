"""
Root of the Panther UI module
"""


class EventManager:
    def __init__(self):
        self.events = {}

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

    def on(self, event):
        """
        Register an event function using this as a function decorator.
        e.g:
            @on('init')
            function init():
                ...
        :param event: string, name of event
        :return:
        """
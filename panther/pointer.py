"""
higher-level pointer events API
"""
import threading
import panther


_pointers = {}

_pointer_loc = (0, 0)
_pointer_loc_lock = threading.Lock()


def pointer_loc():
    """
    get the current pointer loc
    :return: tuple<x, y>
    """
    with _pointer_loc_lock:
        return _pointer_loc


class Pointer:
    def __init__(self, uid, x, y, type="click"):
        self.id = uid
        self.type = type
        self.x, self.y = x, y

        self.points = [(x, y)]

        self.expired = False


@panther.events.on('mousepos')
def mouse_pos(pos):
    """
    Update the _pointer_loc
    :param pos: (x, y)
    :return: None
    """
    global _pointer_loc
    with _pointer_loc_lock:
        _pointer_loc = pos


@panther.events.on('touchdown')
def touch_down(touch):
    """
    Add a new Pointer to the pointers
    :return: None
    """
    _pointers[touch.uid] = Pointer(
        touch.uid,
        touch.x,
        touch.y,
        "click" if touch.device == "mouse" else "touch"
    )


@panther.events.on('touchup')
def touch_up(touch):
    """
    remove the Pointer from the pointers
    :return: None
    """
    _pointers[touch.uid].expired = True


@panther.events.on('touchdrag')
def touch_drag(touch):
    """
    Add more points to the Pointer in pointers
    :return: None
    """
    _pointers[touch.uid].points.append((touch.x, touch.y))


def clicks(remove_expired=True):
    """
    returns a list of the clicks which have occurred
    :return: list<Pointer>
    """
    for pointer in tuple(_pointers.keys()):
        if panther.conf.differentiate_between_touches_and_clicks and _pointers[pointer].type == "click":
            yield _pointers[pointer]
        elif not panther.conf.differentiate_between_touches_and_clicks:
            yield _pointers[pointer]

        if _pointers[pointer].expired and remove_expired:
            del _pointers[pointer]


def touches(remove_expired=True):
    """
    returns a list of the touches which have occurred
    :return:
    """
    for pointer in tuple(_pointers.keys()):
        if panther.conf.differentiate_between_touches_and_clicks and _pointers[pointer].type == "touch":
            yield _pointers[pointer]
        elif not panther.conf.differentiate_between_touches_and_clicks:
            yield _pointers[pointer]

        if _pointers[pointer].expired and remove_expired:
            _pointers.pop(pointer)

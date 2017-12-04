"""
Abstract away from the basic panther.events supplied event model for keypresses
"""
from collections import defaultdict
import panther

_keys = defaultdict(bool)


@panther.events.on("keydown")
def _update_key_down(keyboard, keycode, text, modifiers):
    """
    update the key in _keys to True
    :param keyboard: Keyboard object
    :param keycode: tuple<int(key unicode id), str(key name)> - we use the str key name since it's nicer
    :param text:
    :param modifiers:
    :return: None
    """
    _keys[keycode[1]] = True


@panther.events.on("keyup")
def _update_key_up(keyboard, keycode):
    """
    update the key in _keys to False
    :param keyboard: Keyboard object
    :param keycode: tuple<int(key unicode id), str(key name)> - we use the str key name since it's nicer
    :return: None
    """
    _keys[keycode[1]] = False


def down(keyname):
    """
    whether or not <key> is currently pressed
    :param keyname: string
    :return: bool
    """
    return _keys[keyname]

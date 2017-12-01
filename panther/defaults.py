import time
import panther


def default_run():
    """
    The default run function
    :return: None
    """
    panther.events.trigger_event('load')

    dt = 0

    while True:
        # process events
        if panther.events:
            for event in panther.events:
                print(event)

        panther.draw_screen()
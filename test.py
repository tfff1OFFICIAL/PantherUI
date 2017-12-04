import panther
from panther import graphics


col = [0, 0, 0]


@panther.events.on('load')
def load_event():
    print("Loaded panther!")


@panther.events.on('touchdown')
def touchdown(touch):
    print("touched")


def update_colour():
    global col

    if col[0] <= 255:
        col[0] += 1
    elif col[1] <= 255:
        col[1] += 1
    elif col[2] <= 255:
        col[2] += 1
    else:
        col = [0, 0, 0]


@panther.events.on('draw')
def draw():

    update_colour()

    graphics.set_background_color(col)

    graphics.set_colour("FF0000")
    graphics.circle(50, 50, 10)


panther.conf.height = 500
panther.conf.width = 500
panther.conf.title = "hi there"

panther.start()

from kivy.graphics import Line
import panther
from panther import graphics, key

x, y = 0, 0
touches = dict()


@panther.events.on('quit')
def exit_event():
    print("exiting...")


@panther.events.on('load')
def load_event():
    print("Loaded panther!")


@panther.events.on('touchdown')
def touchdown(touch):
    global touches

    print("touched")
    touches[touch.id] = (touch.x, touch.y)


@panther.events.on("touchdrag")
def touch_drag(touch):
    global touches

    touches[touch.id] += (touch.x, touch.y)


@panther.events.on('update')
def update(dt):
    global x, y

    if not key.down("spacebar"):
        x += 1
        y += 1

    if key.down('escape'):
        panther.quit()


@panther.events.on('draw')
def draw():
    #print(f"drawing on canvas size: {panther.canvas.size}")
    global x, y
    graphics.set_background_color("FFFFFF")

    graphics.set_colour("FF0000")
    graphics.circle(x, y, 10)

    for touch in touches:
        graphics.line(points=touches[touch])

    graphics.set_colour("FFFFFF")
    graphics.image(0, 0, 83, 75, "examples\\smiley.png")


@panther.events.on('resize')
def on_resize(window, width, height):
    print(f"resized to: {width}x{height}")

#panther.conf.height = 500
#panther.conf.width = 500
#panther.conf.title = "hi there"
#panther.conf.clear_every_frame = True

panther.conf.load_from_file('examples/test_config.json')

panther.start()

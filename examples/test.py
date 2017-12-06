from kivy.graphics import Line
import panther
from panther import graphics, key, pointer

x, y = 0, 0
touches = dict()


@panther.events.on('quit')
def exit_event():
    print("exiting...")


@panther.events.on('load')
def load_event():
    print("Loaded panther!")

'''
@panther.events.on('touchdown')
def touchdown(touch):
    global touches

    print("touched")
    touches[touch.id] = (touch.x, touch.y)


@panther.events.on("touchdrag")
def touch_drag(touch):
    global touches

    touches[touch.id] += (touch.x, touch.y)
'''


@panther.events.on('update')
def update(dt):
    global x, y

    if not key.down("spacebar"):
        x += 1
        y += 1

    if key.down('escape'):
        panther.quit()

    panther.conf.title = f"title: {x}"


@panther.events.on('draw')
def draw():
    #print(f"drawing on canvas size: {panther.canvas.size}")
    global x, y
    graphics.set_background_color("FFFFFF")

    graphics.set_colour("FF0000")
    graphics.circle(x, y, 10)

    for point in pointer.clicks(remove_expired=False):
        print(point, end=", ")
        graphics.line(points=point.points)

    mouse_x, mouse_y = pointer.pointer_loc()

    print("MOUSE: x: {}, y: {}".format(mouse_x, mouse_y))

    graphics.set_colour((255, 0, 0, 0.7))
    graphics.regular_polygon(50, 9, 250, 250)
    graphics.polygon(
        (mouse_x, mouse_y),
        (mouse_x+13, mouse_y+6),
        (mouse_x+7, mouse_y-2),
        (mouse_x+10, mouse_y-11),
        (mouse_x, mouse_y)
    )

    #graphics.circle(
    #    (mouse_x - 2),
    #    (mouse_y - 2),
    #    4,
    #    4
    #)

    #for touch in touches:
    #    graphics.line(points=touches[touch])

    graphics.set_colour("FFFFFF")
    graphics.image(0, 0, 83, 75, "examples\\smiley.png")

    graphics.set_colour((255, 128, 000, 1))
    graphics.text(
        200,
        420,
        "test"
    )


@panther.events.on('resize')
def on_resize(w, h, apply_func):
    print(f"resized to: {w}x{h}")
    if h <= 600 and w <= 1000:
        print("applying...")
        apply_func()
    else:
        panther.conf.width = 1000
        panther.conf.height = 600

#panther.conf.height = 500
#panther.conf.width = 500
#panther.conf.title = "hi there"
#panther.conf.clear_every_frame = True

panther.conf.load_from_file('examples/test_config.json')

panther.start()

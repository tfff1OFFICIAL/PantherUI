"""
Testing the multi-layer advanced functionality of Panther
"""
import panther
from panther import key


layer2 = panther.layers.add()


@layer2.events.on("load")
@layer2.locals
def l2_load(locals):
    locals.x = 0
    locals.y = 0

    print("Layer 2 loaded!")


@layer2.events.on("update")
@layer2.locals
def u(locals, dt):
    locals.x += 1
    locals.y += 1

    if locals.x % 70 != 0:
        layer2.clear_next_frame = False
    else:
        layer2.clear_next_frame = True


@layer2.events.on("draw")
@layer2.locals
def l2_draw(locals, graphics):
    graphics.set_colour("FF0000")
    print(f"drawing circle at: ({locals.x}, {locals.y})")
    graphics.circle(locals.x, locals.y, 25)


@panther.events.on("load")
def load():
    print("loaded")

    l3 = panther.layers.add()

    @l3.events.subscribe_to("load")
    def l():
        print("Layer 3 loaded!")

    @l3.events.on("update")
    def update(dt):
        if key.down("escape"):
            panther.quit()

    @l3.events.on("draw")
    def draw(graphics: panther.GraphicsManager):
        graphics.set_colour("FFFFFF")
        graphics.circle(50, 50, 25)


@panther.events.on("update")
def update(dt):
    pass


@panther.events.on("draw")
def draw():
    panther.graphics.set_colour("00FF00")
    panther.graphics.rectangle(10, 10, 5, 5)

panther.start()
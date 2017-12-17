"""
Testing the multi-layer advanced functionality of Panther
"""
import panther
from panther import key


layer2 = panther.layers.add()


@layer2.events.on("load")
@layer2.locals
def l2_load(locals):
    locals.x = 50

    print("Layer 2 loaded!")


@layer2.events.on("update")
@layer2.locals
def u(locals, dt):
    print(locals)
    print(locals.x)
    locals.x += 1


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


@panther.events.on("update")
def update(dt):
    pass


@panther.events.on("draw")
def draw():
    pass

panther.start()
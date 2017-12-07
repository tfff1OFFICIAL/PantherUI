import panther
from panther import graphics, key

square_move_x = 0
square_move_y = 0


@panther.events.on('update')
def update_handler(dt):
    global square_move_x, square_move_y
    if not key.down("spacebar"):
        if square_move_x != panther.conf.width / 2:  # if the square is still on the screen
            square_move_x += 1
        else:
            square_move_x = 0

        if square_move_y != panther.conf.height / 2:  # if the square is still on the screen
            square_move_y += 1
        else:
            square_move_y = 0


@panther.events.on('draw')
def draw():
    global square_move_x, square_move_y

    graphics.rectangle(
        x=panther.conf.width / 2 - 20 + square_move_x,
        y=panther.conf.height / 2 - 20 + square_move_y,
        width=40,
        height=40
    )


panther.start()#width=400, height=400)
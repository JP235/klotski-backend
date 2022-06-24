from .custom_types import MoveDirection

CODE_LENGTH = 4

EMP = "--"
WIN_NAME = "GG"

UP = MoveDirection("UP")
LEFT = MoveDirection("LEFT")
DOWN = MoveDirection("DOWN")
RIGHT = MoveDirection("RIGHT")

MOVES = [
    (UP, "UP"),
    (LEFT, "LEFT"),
    (DOWN, "DOWN"),
    (RIGHT, "RIGHT"),
]

OPP_MOVES = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

IMG_WIN = "img_win"
IMG_CURR = "img_curr"

IMG_WIN_PATH = "win"
IMG_CURR_PATH = "curr"
from .constants import UP, DOWN, LEFT, RIGHT

def delts_to_move(dx,dy):
    if dx == 1 and dy == 0:
        return DOWN
    elif dx == 0 and dy == -1:
        return LEFT
    elif dx == -1 and dy ==0:
        return UP
    elif dx == 0 and dy == 1:
        return RIGHT
    else:
        print(f"{dx=}, {dy=}")
        raise ValueError("Invalid deltas")

def move_to_delts(move):
    if move == UP:
        return (-1, 0)
    elif move == LEFT:
        return (0, -1)
    elif move == DOWN:
        return (1, 0)
    elif move == RIGHT:
        return (0, 1)
    else:
        print(f"{move=}")
        raise ValueError("Invalid move")

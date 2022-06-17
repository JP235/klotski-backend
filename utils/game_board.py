import numpy as np

from .errors import OverlarpingBlocksError
from .constants import EMP, WIN_NAME


def make_game_board(game, board_only=True):
    board = np.full((game.rows, game.cols), EMP)
    blocks = game.game_blocks.all()
    empty_sp = np.array([True for _ in range(game.rows * game.cols)])
    bl_xy = {}

    for block in blocks:
        for coord in block.coords:
            if empty_sp[coord[0] * game.cols + coord[1]]:
                board[coord] = block.name
                empty_sp[coord[0] * game.cols + coord[1]] = False
            else:
                raise OverlarpingBlocksError(
                    f"Block {block.name} overlaps with another block"
                )
            bl_xy.setdefault(block.name, []).append(coord)

    if board_only:
        return board

    win_x = game.win_block_x
    win_y = game.win_block_y
    win_board = np.full((game.rows, game.cols), EMP)
    win_board[win_x, win_y] = WIN_NAME

    return board, bl_xy, win_board 


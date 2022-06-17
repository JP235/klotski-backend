from .custom_types import Board
import numpy as np

def bad_stringify(board:Board):
    """
    badly Stringify an object.
    """
    if board is not None:
        return "-".join(board.flatten())
    return None
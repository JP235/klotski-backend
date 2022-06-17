from .constants import OPP_MOVES
from .custom_types import MovesHistory, BlMove

def is_next_move_opposite(history: MovesHistory, move: BlMove) -> bool:
    """
    Returns True if move is opposite to last move in history.
    """
    try:
        name1,move1  = history[-1]
        # = history[-1]
    except IndexError: # history is empty
        return False
    except TypeError: # history is None
        return False

    name2 = move[0]
    move2 = move[1]

    if name1 != name2:
        return False

    if move1 == OPP_MOVES[move2]:
        return True
    
    return False

from typing import NewType
import numpy as np

BlName = NewType("BlName", str)
MoveDirection = NewType("MoveDirection", str)

BlMove = NewType("BlockMove", tuple[BlName, MoveDirection])
MovesHistory = NewType("MovesHistory", list[BlMove])

Board = NewType("Board", np.ndarray)
BoardDict = NewType("BoardDict", dict[BlName, tuple[int, int]])
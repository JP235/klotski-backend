
class CodeGenerationError(Exception):
    """Code generation error"""

class OutOfBoardError(IndexError): 
    """Move ends up out of board"""

class OverlarpingBlocksError(ValueError): 
    """Move ends up overlaping blocks"""
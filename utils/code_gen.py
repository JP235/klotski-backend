import random
import string
from .errors import CodeGenerationError
from .constants import CODE_LENGTH

def generate_unique_code() -> str:
    from game.models import GameKlotski # import inside function to avoid circular import
    tries = 0
    while tries < 10 ** CODE_LENGTH:
        tries += 1
        code = "".join(random.choices(string.ascii_uppercase, k=CODE_LENGTH))
        if GameKlotski.objects.filter(code=code).count() == 0:
            return code
    raise CodeGenerationError("Could not generate unique code")

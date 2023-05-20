import random as rn
from dna_mapping import bits_to_dna
from utils import gc_content

random_choice = lambda s, i, r: rn.choice(r)


def gc_tracking(
    state: str,
    input: str,
    reserved: list[str],
    gc_target: float = 0.5,
) -> str:
    closest = None
    least = 1

    for bits in reserved:
        concat = state + bits + input
        gc = gc_content(bits_to_dna(concat))
        diff = abs(gc_target - gc)

        if diff == 0:
            return bits

        if diff < least:
            least = diff
            closest = bits

    return closest

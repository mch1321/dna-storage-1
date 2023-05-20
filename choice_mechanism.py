import random as rn
from dna_mapping import bits_to_dna
from utils import gc_content, hamming_dist

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


def gc_tracked_random(
    state: str,
    input: str,
    reserved: list[str],
    gc_target: float = 0.5,
) -> str:
    least = 1
    opt_gc = []

    for bits in reserved:
        concat = state + bits + input
        gc = gc_content(bits_to_dna(concat))
        diff = abs(gc_target - gc)

        if diff < least:
            least = diff
            opt_gc = [bits]
        elif diff == least:
            opt_gc.append(bits)

    return rn.choice(opt_gc)


def max_hamming(
    state: str,
    input: str,
    reserved: list[str],
) -> str:
    most = 0
    opt = []

    for bits in reserved:
        output = bits + input
        dist = hamming_dist(state, output)

        if dist > most:
            most = dist
            opt = [bits]
        elif dist == most:
            opt.append(bits)

    return rn.choice(opt)


def min_hamming(
    state: str,
    input: str,
    reserved: list[str],
) -> str:
    least = len(state)
    opt = []

    for bits in reserved:
        output = bits + input
        dist = hamming_dist(state, output)

        if dist < least:
            least = dist
            opt = [bits]
        elif dist == least:
            opt.append(bits)

    return rn.choice(opt)

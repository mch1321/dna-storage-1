import numpy as np
import random as rn
from data_types import Transition


def table_from_list(transitions: list[Transition]):
    table = {}

    for transition in transitions:
        if transition.start not in table:
            table[transition.start] = {transition.input: transition}
        else:
            table[transition.start][transition.input] = transition

    return table


def table_from_matrix(states, inputs, matrix):
    transitions = []
    for i, state in enumerate(states):
        for j, input in enumerate(inputs):
            transitions.append(
                Transition(
                    start=state,
                    next=matrix[i][j][0],
                    input=input,
                    output=matrix[i][j][1],
                )
            )
    return table_from_list(transitions)


def beautify_table(table):
    result = "{\n"
    for state in table:
        result += f"    {state}:"
        result += " {\n"
        for input in table[state]:
            next = table[state][input].next
            output = table[state][input].output
            result += f"        {input} -> next: {next}, output: {output}\n"
        result += "    },\n"
    result += "}"
    return result


def hamming_dist(one: str, two: str) -> int:
    assert len(one) == len(two)

    dist = 0
    for a, b in zip(list(one), list(two)):
        if a != b:
            dist += 1
    return dist


def burst_score(true: str, pred: str) -> int:
    assert len(true) == len(pred)

    burst = 0
    score = 0

    for t, p in zip(list(true), list(pred)):
        if t != p:
            burst += 1
            if burst == 2:
                score += 2
            elif burst > 2:
                score += 1
        else:
            burst = 0

    return score


def strs(sequence: str, size: int = 4) -> int:
    count = 0
    for i in range(len(sequence) - size * 2):
        one = sequence[i : i + size]
        two = sequence[i + size : i + size * 2]
        if one == two:
            count += 1
    return count


def rand_bit_string(length: int) -> str:
    bits = ""
    for i in range(length):
        if rn.random() < 0.5:
            bits += "0"
        else:
            bits += "1"
    return bits


def inject_bit_errors(message: str, rate: float = 0.01) -> str:
    result = ""
    for bit in message:
        if rn.random() <= rate:
            result += "0" if bit == "1" else "1"
        else:
            result += bit
    return result


def rand_base(exclude: str = ""):
    bases = "ACGT".replace(exclude, "")
    return rn.choice(bases)


def rand_bases(exclude: str, length: int) -> str:
    bases = "ACGT"
    for e in exclude:
        bases = bases.replace(e, "")
    return "".join([rn.choice(bases) for _ in range(length)])


def inject_base_errors(message: str, rate: float = 0.01) -> str:
    result = ""
    for base in message:
        if rn.random() <= rate:
            result += rand_base(base)
        else:
            result += base
    return result


def inject_burst_errors(
    message: str, rate: float = 0.01, min_burst=2, max_burst=4
) -> str:
    result = message[:]

    num_errors = int(len(message) * rate)

    # Injects ROUGHLY num_errors many errors into the message.
    while num_errors > 0:
        burst = rn.randint(min_burst, max_burst)
        position = rn.randrange(len(message) - burst)

        error = ""
        for i in range(burst):
            error += rand_base(message[position + i])

        result = result[:position] + error + result[position + burst :]

        num_errors -= burst

    return result


def inject_deletion_errors(message: str, rate: float = 0.01) -> str:
    result = ""
    for base in message:
        if rn.random() > rate:
            result += base
    return result


def inject_insertion_errors(message: str, rate: float = 0.01) -> str:
    result = ""
    for base in message:
        if rn.random() <= rate:
            result += rand_base()
        result += base
    return result


# Injects a precise number of errors at random locations.
def inject_base_errors_exact(message: str, num: int) -> str:
    result = list(message)
    if len(message) < num:
        raise Exception("Number of errors too high for message length.")
    locations = rn.sample(range(len(message)), num)
    for i in locations:
        result[i] = rand_base(exclude=result[i])
    return "".join(result)


def sequence_is_valid(sequence: str) -> bool:
    return all([base in "ACGT" for base in sequence])


def contains_reserved(sequence: str, reserved: list[str]) -> bool:
    for r in reserved:
        if len(r) > len(sequence):
            raise Exception(f"Reserved subsequence is longer than the given sequence.")
        if r in sequence:
            return True
    return False


def gc_content(sequence: str) -> float:
    gc = 0
    for base in sequence:
        if base not in "ACGT":
            raise Exception(f"Sequence contains invalid symbol {base}.")
        if base in "GC":
            gc += 1
    return float(gc) / float(len(sequence))


def max_gc_variance(sequence: str, window: int = 4, step: int = 1) -> float:
    gc = gc_content(sequence[0:window])
    min_gc = gc
    max_gc = gc
    for i in range(1, len(sequence) - window + 1, step):
        section = sequence[i : min(i + window, len(sequence))]
        gc = gc_content(section)
        if gc < min_gc:
            min_gc = gc
        elif gc > max_gc:
            max_gc = gc

    return max_gc - min_gc


def longest_homopolymer(sequence: str) -> int:
    longest = 0
    count = 0
    curr = sequence[0]

    for base in sequence:
        if base not in "ACGT":
            raise Exception(f"Sequence contains invalid symbol {base}.")

        if base == curr:
            count += 1
            if count > longest:
                longest = count
        else:
            count = 1

        curr = base

    return longest


def base_idx(base: str) -> int:
    if base == "A":
        return 0
    elif base == "C":
        return 1
    elif base == "G":
        return 2
    elif base == "T":
        return 3
    else:
        raise Exception(f"Invalid base {base}.")


def confusion(true: str, pred: str) -> np.ndarray:
    confusion = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    for t, p in zip(true, pred):
        confusion[base_idx(t)][base_idx(p)] += 1

    return confusion


if __name__ == "__main__":
    print(gc_content("AAAAAAAA") == 0)
    print(gc_content("ACGTACGT") == 0.5)
    print(gc_content("AACGTCCC") == 5.0 / 8.0)
    print(gc_content("TTTTACCC") == 3.0 / 8.0)
    print(gc_content("TTTTATTT") == 0)

    print(longest_homopolymer("AAAAAAAA") == 8)
    print(longest_homopolymer("ACGTACGT") == 1)
    print(longest_homopolymer("AACGTCCC") == 3)
    print(longest_homopolymer("TTTTACCC") == 4)
    print(longest_homopolymer("TTTTATTT") == 4)

    print(burst_score("ACGTACGT", "ACGTACGT"))
    print(burst_score("ACGTACGT", "AAGAAAGT"))
    print(burst_score("ACGTACGT", "AAATAAGT"))
    print(burst_score("ACGTACGT", "AAAAAAAA"))
    print(burst_score("ACGTACGT", "AAAATAAA"))

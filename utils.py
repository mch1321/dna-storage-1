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
    for i in range(len(one)):
        if one[i] != two[i]:
            dist += 1
    return dist


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
    index = rn.randrange(len(bases))
    return bases[index]


def inject_base_errors(message: str, rate: float = 0.01) -> str:
    result = ""
    for base in message:
        if rn.random() <= rate:
            result += rand_base(base)
        else:
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

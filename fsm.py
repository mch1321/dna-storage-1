import math
from constraints import Constraints
from data_types import Path, Transition
from dna_mapping import bits_to_dna
from utils import hamming_dist, table_from_list


class FSM:
    def __init__(
        self, init_state: str, transition_table, input_size: int, output_size: int
    ):
        self.init_state = init_state
        self.table = transition_table
        self.input_size = input_size
        self.output_size = output_size

    def conv(self, message: str) -> str:
        if len(message) % self.input_size != 0:
            raise Exception(
                "The length of the input message must be a multiple of the input size."
            )

        result = ""
        state = self.init_state

        for i in range(0, len(message), self.input_size):
            symbol = message[i : i + self.input_size]
            new = self.table[state][symbol]

            if new is None:
                raise Exception(f"Invalid input {symbol} has no transition in table.")

            state = new.next
            result += new.output

        return result

    def viterbi(self, received: str) -> str:
        if len(received) % self.output_size != 0:
            raise Exception(
                "The length of the received message must be a multiple of the symbol size."
            )

        paths = {self.init_state: Path(self.init_state)}

        for i in range(0, len(received), self.output_size):
            symbol = received[i : i + self.output_size]
            extended_paths = {}
            for path in paths.values():
                for t in self.table[path.tip].values():
                    dist = hamming_dist(symbol, t.output)
                    extended = path.copy()
                    extended.extend(t.next, dist, t.input, t.output)

                    if (
                        t.next not in extended_paths
                        or extended.length < extended_paths[t.next].length
                    ):
                        extended_paths[t.next] = extended

            paths = extended_paths

        min_dist = math.inf
        shortest = None
        for path in paths.values():
            if path.length < min_dist:
                min_dist = path.length
                shortest = path

        assert shortest is not None
        return shortest


def populate_space(size: int) -> list[str]:
    space = []
    dim = 2**size  # Size of the space
    for i in range(dim):
        b = bin(i).removeprefix("0b")
        padding = size - len(b)
        space.append(padding * "0" + b)
    return space


def table_from_constraints(
    input_size: int,
    output_size: int,
    constraints: Constraints,
    choice_mechanism: callable,
):
    if input_size >= output_size:
        raise Exception("Input/trigger size must be less than the output/symbol size.")

    transitions = []

    reserved_size = output_size - input_size
    states = populate_space(output_size)  # Horizontal Symbols
    inputs = populate_space(input_size)  # Vertical Symbols
    reserved = populate_space(reserved_size)  # Reserved bits

    for s in states:
        for i in inputs:
            candidates = []
            for r in reserved:
                if constraints.satisfied(bits_to_dna(s + r + i)):
                    candidates.append(r)
            if len(candidates) == 0:
                raise Exception("Impossible to meet constraints")
            chosen = choice_mechanism(s, i, candidates)
            output = chosen + i
            transitions.append(Transition(start=s, input=i, output=output, next=output))

    return table_from_list(transitions)


def construct_fsm_from_constraints(
    init_state: str,
    input_size: int,
    output_size: int,
    constraints: Constraints,
    choice_mechanism: callable,
) -> FSM:
    table = table_from_constraints(
        input_size, output_size, constraints, choice_mechanism
    )
    return FSM(init_state, table, input_size, output_size)

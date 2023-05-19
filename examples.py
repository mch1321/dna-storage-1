from choice_mechanism import random_choice
from constraints import default_constraints
from data_types import Path, Transition
from dna_mapping import bits_to_dna, dna_to_bits
from fsm import construct_fsm_from_constraints, FSM
from utils import (
    hamming_dist,
    inject_bit_errors,
    beautify_table,
    table_from_list,
    table_from_matrix,
)

EXAMPLE_MESSAGE = "001010101110010001010110110110100010111010100110011110010001"


def constructing_transition_tables():
    states = ["00", "01", "10", "11"]
    inputs = ["0", "1"]

    transition_matrix = [
        [("00", "00"), ("10", "11")],
        [("00", "11"), ("10", "00")],
        [("01", "01"), ("11", "10")],
        [("10", "10"), ("11", "01")],
    ]

    t = [
        Transition(start="00", input="0", output="00", next="00"),
        Transition(start="00", input="1", output="11", next="10"),
        Transition(start="01", input="0", output="11", next="00"),
        Transition(start="01", input="1", output="00", next="10"),
        Transition(start="10", input="0", output="01", next="01"),
        Transition(start="10", input="1", output="10", next="11"),
        Transition(start="11", input="0", output="10", next="10"),
        Transition(start="11", input="1", output="01", next="11"),
    ]

    from_list = table_from_list(t)
    from_matrix = table_from_matrix(states, inputs, transition_matrix)

    if from_list != from_matrix:
        raise Exception("Error found in transition table methods")

    print(beautify_table(from_list))


def one_half(eg=EXAMPLE_MESSAGE, output=True):
    initState = "00"
    states = ["00", "01", "10", "11"]
    inputs = ["0", "1"]

    transition_matrix = [
        [("00", "00"), ("10", "11")],
        [("00", "11"), ("10", "00")],
        [("01", "01"), ("11", "10")],
        [("10", "10"), ("11", "01")],
    ]

    initState = "00"
    table = table_from_matrix(states, inputs, transition_matrix)

    fsm: FSM = FSM(initState, table, 1, 2)

    enc = fsm.conv(eg)
    path: Path = fsm.viterbi(enc)

    if output:
        print(f"ONE HALF ENCODING WITHOUT ERRORS")
        print(f"Raw message        : {eg}")
        print(f"Encoded message    : {enc}")
        print(f"Viterbi path       : {path.observations}")
        print(f"Decoded message    : {path.sequence}")
        print(f"Found correct path : {enc == path.observations}")
        print(f"Correctly decoded  : {eg == path.sequence}")
        print("----------------------------------------------------")

    return enc, fsm


def one_half_with_errors(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    enc, fsm = one_half(eg=eg, output=False)

    err = inject_bit_errors(enc, error_rate)
    path: Path = fsm.viterbi(err)

    if output:
        print(f"ONE HALF ENCODING WITH ERROR RATE {error_rate}")
        print(f"Raw message      : {eg}")
        print(f"Encoded message  : {enc}")
        print(f"Received message : {err}")
        print(f"Viterbi path     : {path.observations}")
        print(f"Decoded message  : {path.sequence}")
        print(f"Errors injected  : {hamming_dist(enc, err)}")
        print(f"Errors remaining : {hamming_dist(enc, path.observations)}")
        print(f"After decoding   : {hamming_dist(eg, path.sequence)}")
        print("----------------------------------------------------")


def two_thirds(eg=EXAMPLE_MESSAGE, output=True):
    initState = "0"
    states = ["0", "1", "2", "3", "4", "5", "6", "7"]
    inputs = ["00", "01", "10", "11"]

    transition_matrix = [
        [("0", "000"), ("1", "100"), ("2", "010"), ("3", "110")],
        [("4", "001"), ("5", "101"), ("6", "011"), ("7", "111")],
        [("1", "100"), ("0", "000"), ("3", "110"), ("2", "010")],
        [("5", "101"), ("4", "001"), ("7", "111"), ("6", "011")],
        [("2", "010"), ("3", "110"), ("0", "000"), ("1", "100")],
        [("6", "011"), ("7", "111"), ("4", "001"), ("5", "101")],
        [("3", "110"), ("2", "010"), ("1", "100"), ("0", "000")],
        [("7", "111"), ("6", "011"), ("5", "101"), ("4", "011")],
    ]

    transitions = table_from_matrix(states, inputs, transition_matrix)
    fsm: FSM = FSM(initState, transitions, 2, 3)

    enc = fsm.conv(eg)
    path: Path = fsm.viterbi(enc)

    if output:
        print(f"TWO THIRDS ENCODING WITHOUT ERRORS")
        print(f"Raw message        : {eg}")
        print(f"Encoded message    : {enc}")
        print(f"Viterbi path       : {path.observations}")
        print(f"Decoded message    : {path.sequence}")
        print(f"Found correct path : {enc == path.observations}")
        print(f"Correctly decoded  : {eg == path.sequence}")
        print("----------------------------------------------------")

    return enc, fsm


def two_thirds_with_errors(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    enc, fsm = two_thirds(eg=eg, output=False)

    err = inject_bit_errors(enc, error_rate)
    path: Path = fsm.viterbi(err)

    if output:
        print(f"TWO THIRDS ENCODING WITH ERROR RATE {error_rate}")
        print(f"Raw message      : {eg}")
        print(f"Encoded message  : {enc}")
        print(f"Received message : {err}")
        print(f"Viterbi path     : {path.observations}")
        print(f"Decoded message  : {path.sequence}")
        print(f"Errors injected  : {hamming_dist(enc, err)}")
        print(f"Errors remaining : {hamming_dist(enc, path.observations)}")
        print(f"After decoding   : {hamming_dist(eg, path.sequence)}")
        print("----------------------------------------------------")


def dna_round_trip(eg=EXAMPLE_MESSAGE, output=True):
    symbol_size = 4
    reserved_bits = 5

    output_size = 2 * symbol_size
    input_size = output_size - reserved_bits
    init_state = output_size * "0"

    fsm = construct_fsm_from_constraints(
        init_state, input_size, output_size, default_constraints(), random_choice
    )

    enc = fsm.conv(eg)
    dna = bits_to_dna(enc)
    path = fsm.viterbi(dna_to_bits(dna))

    if output:
        print(f"DNA ROUND TRIP WITHOUT ERRORS")

        print(f"Raw message        : {eg}")
        print(f"Encoded message    : {enc}")
        print(f"DNA message        : {dna}")
        print(f"Viterbi path       : {path.observations}")
        print(f"Decoded message    : {path.sequence}")
        print(f"Found correct path : {enc == path.observations}")
        print(f"Correctly decoded  : {eg == path.sequence}")
        print("----------------------------------------------------")

    return dna, fsm


def run_all_examples():
    constructing_transition_tables()
    one_half()
    one_half_with_errors()
    two_thirds()
    two_thirds_with_errors()
    dna_round_trip()


if __name__ == "__main__":
    run_all_examples()

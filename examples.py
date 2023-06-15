import viterbi
import encoding
import numpy as np
import random as rn
from choice_mechanism import gc_tracking, random_choice
from constraints import default_constraints
from data_types import Path, Transition
from dna_mapping import bits_to_dna, dna_to_bits
from fsm import construct_fsm_from_constraints, FSM
from utils import (
    hamming_dist,
    inject_base_errors,
    inject_bit_errors,
    beautify_table,
    table_from_list,
    table_from_matrix,
    rand_bit_string,
    gc_content,
)

EXAMPLE_MESSAGE = "001010101110010001010110110110100010111010100110011110010001"
LONGER_MESSAGE = "001010101110010001010110110110100010111010100110011110010001001010101110010001010110110110100010111010100110011110010001"


def constructing_transition_tables(output=True):
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

    if output:
        print(beautify_table(from_list))
    return from_list


def one_half(eg=EXAMPLE_MESSAGE, output=True):
    init_state = "00"
    states = ["00", "01", "10", "11"]
    inputs = ["0", "1"]

    transition_matrix = [
        [("00", "00"), ("10", "11")],
        [("00", "11"), ("10", "00")],
        [("01", "01"), ("11", "10")],
        [("10", "10"), ("11", "01")],
    ]

    init_state = "00"
    table = table_from_matrix(states, inputs, transition_matrix)

    fsm: FSM = FSM(init_state, table, 1, 2)

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
    init_state = "0"
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
    fsm: FSM = FSM(init_state, transitions, 2, 3)

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

    easy_constraints = default_constraints()
    # easy_constraints.gc_max = 0.85
    # easy_constraints.gc_min = 0.15

    fsm = construct_fsm_from_constraints(
        init_state, input_size, output_size, easy_constraints, random_choice
    )

    enc = fsm.conv(eg)
    dna = bits_to_dna(enc)
    path = fsm.viterbi(dna_to_bits(dna))

    if output:
        print("DNA ROUND TRIP WITHOUT ERRORS")

        print(f"Raw message        : {eg}")
        print(f"Encoded message    : {enc}")
        print(f"DNA message        : {dna}")
        print(f"Viterbi path       : {path.observations}")
        print(f"Decoded message    : {path.sequence}")
        print(f"Found correct path : {enc == path.observations}")
        print(f"Correctly decoded  : {eg == path.sequence}")
        print(f"GC Content         : {gc_content(dna)}")
        print("----------------------------------------------------")

    return dna, enc, fsm


def dna_round_trip_with_errors(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    dna, enc, fsm = dna_round_trip(eg, output=False)
    dna_err = inject_base_errors(dna, error_rate)
    err = dna_to_bits(dna_err)
    path = fsm.viterbi(err)
    dna_cor = bits_to_dna(path.observations)

    if output:
        print(f"DNA ROUND TRIP WITH ERROR RATE {error_rate}")
        print(f"Raw message      : {eg}")
        print(f"Encoded message  : {enc}")
        print(f"DNA message      : {dna}")
        print(f"Received message : {dna_err}")
        print(f"Corrected DNA    : {dna_cor}")
        print(f"Viterbi path     : {path.observations}")
        print(f"Decoded message  : {path.sequence}")
        print(f"Errors injected  : {hamming_dist(enc, err)}")
        print(f"Errors remaining : {hamming_dist(enc, path.observations)}")
        print(f"After decoding   : {hamming_dist(eg, path.sequence)}")
        print(f"GC Content       : {gc_content(dna)}")
        print("----------------------------------------------------")

    return dna, fsm


def dna_gc_tracking(eg=EXAMPLE_MESSAGE, output=True):
    symbol_size = 4
    reserved_bits = 5

    output_size = 2 * symbol_size
    input_size = output_size - reserved_bits
    init_state = output_size * "0"

    fsm = construct_fsm_from_constraints(
        init_state, input_size, output_size, default_constraints(), gc_tracking
    )

    enc = fsm.conv(eg)
    dna = bits_to_dna(enc)
    path = fsm.viterbi(dna_to_bits(dna))

    if output:
        print("DNA GC TRACKING WITHOUT ERRORS")

        print(f"Raw message        : {eg}")
        print(f"Encoded message    : {enc}")
        print(f"DNA message        : {dna}")
        print(f"Viterbi path       : {path.observations}")
        print(f"Decoded message    : {path.sequence}")
        print(f"Found correct path : {enc == path.observations}")
        print(f"Correctly decoded  : {eg == path.sequence}")
        print(f"GC Content         : {gc_content(dna)}")
        print("----------------------------------------------------")

    return dna, enc, fsm


def dna_gc_tracking_with_errors(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    dna, enc, fsm = dna_gc_tracking(eg, output=False)
    dna_err = inject_base_errors(dna, error_rate)
    err = dna_to_bits(dna_err)
    path = fsm.viterbi(err)
    dna_cor = bits_to_dna(path.observations)

    if output:
        print(f"DNA GC TRACKING WITH ERROR RATE {error_rate}")
        print(f"Raw message      : {eg}")
        print(f"Encoded message  : {enc}")
        print(f"DNA message      : {dna}")
        print(f"Received message : {dna_err}")
        print(f"Corrected DNA    : {dna_cor}")
        print(f"Viterbi path     : {path.observations}")
        print(f"Decoded message  : {path.sequence}")
        print(f"Errors injected  : {hamming_dist(enc, err)}")
        print(f"Errors remaining : {hamming_dist(enc, path.observations)}")
        print(f"After decoding   : {hamming_dist(eg, path.sequence)}")
        print(f"GC Content       : {gc_content(dna)}")
        print("----------------------------------------------------")

    return dna, fsm


def rust_dna_round_trip(eg=EXAMPLE_MESSAGE, output=True):
    symbol_size = 4
    reserved_bits = 5

    output_size = 2 * symbol_size
    input_size = output_size - reserved_bits
    init_state = output_size * "0"

    c = default_constraints()
    constraints = (c.gc_min, c.gc_max, c.max_run_length, c.reserved)
    fsm = encoding.random_fsm(
        symbol_size, reserved_bits, init_state, constraints, 123456
    )

    enc = viterbi.encode(fsm, eg)
    dna = encoding.bits_to_dna(enc)
    (l, seq, obs) = viterbi.decode(fsm, encoding.dna_to_bits(dna))

    if output:
        print("RUST DNA ROUND TRIP WITHOUT ERRORS")

        print(f"Raw message        : {eg}")
        print(f"Encoded message    : {enc}")
        print(f"DNA message        : {dna}")
        print(f"Viterbi path       : {obs}")
        print(f"Decoded message    : {seq}")
        print(f"DNA message correct: {dna == encoding.bits_to_dna(obs)}")
        print(f"Found correct path : {enc == obs}")
        print(f"Correctly decoded  : {eg == seq}")
        print(f"GC Content         : {gc_content(dna)}")
        print("----------------------------------------------------")

    return dna, enc, fsm


def rust_dna_round_trip_with_errors(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    dna, enc, fsm = rust_dna_round_trip(eg, output=False)
    dna_err = inject_base_errors(dna, error_rate)
    err = encoding.dna_to_bits(dna_err)
    (l, seq, obs) = viterbi.decode(fsm, err)
    dna_cor = encoding.bits_to_dna(obs)

    if output:
        print(f"RUST DNA ROUND TRIP WITH ERROR RATE {error_rate}")
        print(f"Raw message      : {eg}")
        print(f"Encoded message  : {enc}")
        print(f"DNA message      : {dna}")
        print(f"Received message : {dna_err}")
        print(f"Corrected DNA    : {dna_cor}")
        print(f"Viterbi path     : {obs}")
        print(f"Decoded message  : {seq}")
        print(f"Errors injected  : {hamming_dist(enc, err)}")
        print(f"Errors remaining : {hamming_dist(enc, obs)}")
        print(f"After decoding   : {hamming_dist(eg, seq)}")
        print(f"GC Content       : {gc_content(dna)}")
        print("----------------------------------------------------")

    return dna, fsm


def rust_python_equivalence(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    python_table = constructing_transition_tables(output=False)
    rust_table = {
        "00": {"0": ("00", "00"), "1": ("10", "11")},
        "01": {"0": ("00", "11"), "1": ("10", "00")},
        "10": {"0": ("01", "01"), "1": ("11", "10")},
        "11": {"0": ("10", "10"), "1": ("11", "01")},
    }

    py_fsm = FSM("00", python_table, 1, 2)
    rust_fsm = (1, 2, "00", rust_table)

    py_enc = py_fsm.conv(eg)
    rust_enc = viterbi.encode(rust_fsm, eg)

    assert rust_enc == py_enc
    err = inject_bit_errors(rust_enc, error_rate)

    py_dec = py_fsm.viterbi(err)
    (l, seq, obs) = viterbi.decode(rust_fsm, err)

    if output:
        print(eg)
        print(py_dec.sequence)
        print(seq)
        print(hamming_dist(py_dec.sequence, seq))
        print(hamming_dist(eg, py_dec.sequence))
        print(hamming_dist(eg, seq))
    return hamming_dist(py_dec.sequence, eg), hamming_dist(seq, eg)


def dna_rust_python_equivalence(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    symbol_size = 4
    reserved_bits = 5

    output_size = 2 * symbol_size
    input_size = output_size - reserved_bits
    init_state = output_size * "0"

    c = default_constraints()
    constraints = (c.gc_min, c.gc_max, c.max_run_length, c.reserved)
    rs_fsm = encoding.random_fsm(
        symbol_size, reserved_bits, init_state, constraints, 3928401
    )

    py_fsm = construct_fsm_from_constraints(
        init_state, input_size, output_size, c, random_choice
    )

    py_enc = py_fsm.conv(eg)
    py_dna = bits_to_dna(py_enc)

    rs_enc = viterbi.encode(rs_fsm, eg)
    rs_dna = encoding.bits_to_dna(rs_enc)

    py_dna_err = inject_base_errors(py_dna, error_rate)
    py_err = dna_to_bits(py_dna_err)
    rs_dna_err = inject_base_errors(rs_dna, error_rate)
    rs_err = encoding.dna_to_bits(rs_dna_err)

    py_path = py_fsm.viterbi(py_err)
    (l, seq, obs) = viterbi.decode(rs_fsm, rs_err)

    if output:
        print(eg)
        print(py_path.sequence)
        print(seq)
        print(hamming_dist(py_path.sequence, seq))
        print(hamming_dist(eg, py_path.sequence))
        print(hamming_dist(eg, seq))

    return hamming_dist(eg, py_path.sequence), hamming_dist(eg, seq)


def rust_one_half_with_errors(eg=EXAMPLE_MESSAGE, error_rate=0.05, output=True):
    fsm = viterbi.one_half()
    enc = viterbi.encode(fsm, eg)
    dna = encoding.bits_to_dna(enc)
    dna_err = inject_base_errors(dna, error_rate)
    err = encoding.dna_to_bits(dna_err)
    (l, seq, obs) = viterbi.decode(fsm, err)
    dna_cor = encoding.bits_to_dna(obs)

    if output:
        print(f"RUST DNA ROUND TRIP WITH ERROR RATE {error_rate}")
        print(f"Raw message      : {eg}")
        print(f"Encoded message  : {enc}")
        print(f"DNA message      : {dna}")
        print(f"Received message : {dna_err}")
        print(f"Corrected DNA    : {dna_cor}")
        print(f"Viterbi path     : {obs}")
        print(f"Decoded message  : {seq}")
        print(f"Errors injected  : {hamming_dist(enc, err)}")
        print(f"Errors remaining : {hamming_dist(enc, obs)}")
        print(f"After decoding   : {hamming_dist(eg, seq)}")
        print(f"GC Content       : {gc_content(dna)}")
        print("----------------------------------------------------")

    return dna, enc, fsm


def run_all_examples():
    # constructing_transition_tables()
    # one_half()
    # one_half_with_errors()
    # two_thirds()
    # two_thirds_with_errors()
    # dna_round_trip()
    # dna_round_trip_with_errors(error_rate=0.05)
    # dna_round_trip_with_errors(eg=rand_bit_string(90))
    # dna_gc_tracking()
    # dna_gc_tracking_with_errors()
    # rust_dna_round_trip()
    # rust_dna_round_trip_with_errors(error_rate=0.05)
    # rust_python_equivalence()
    # dna_rust_python_equivalence()
    rust_one_half_with_errors()


if __name__ == "__main__":
    run_all_examples()

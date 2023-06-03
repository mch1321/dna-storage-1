import copy
import numpy as np
import random as rn
import viterbi
import encoding
from dataclasses import dataclass
from statistics import mean
from choice_mechanism import gc_tracking, gc_tracked_random, random_choice
from constraints import Constraints, default_constraints
from data_types import Path
from dna_mapping import bits_to_dna, dna_to_bits
from fsm import construct_fsm_from_constraints
from utils import confusion, hamming_dist, inject_base_errors, rand_bit_string


@dataclass
class Parameters:
    symbol_size: int = 4
    reserved_bits: int = 5
    choice_mechanism: str = "random"
    constraints: Constraints = default_constraints()
    sequence: str = None
    sequence_length: int = 60
    error_rate: float = 0.05
    repetitions: int = 20
    random_seed: int = None

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return (
            "Parameters:\n"
            + f"    Symbol size: {self.symbol_size}\n"
            + f"    Reserved bits: {self.reserved_bits}\n"
            + f"    Choice mechanism: {self.choice_mechanism}\n"
            + f"    Constraints: {self.constraints.short_str()}\n"
            + (
                f"    Sequence: {self.sequence}\n"
                if self.sequence is not None
                else f"    Sequence length: {self.sequence_length}\n"
            )
            + f"    Error chance: {self.error_rate}\n"
            + f"    Repetitions: {self.repetitions}\n"
            + f"    Random seed: {self.random_seed}\n"
        )


# TODO: Remove rust checks and neaten up
def run_experiment(
    params: Parameters = Parameters(),
    verbose: bool = True,
):
    output_size = 2 * params.symbol_size

    if params.reserved_bits >= output_size:
        raise Exception("Too many reserved bits for given symbol size.")

    input_size = output_size - params.reserved_bits
    init_state = output_size * "0"

    if params.random_seed is not None:
        rn.seed(params.random_seed)

    c = params.constraints
    rs_cons = (c.gc_min, c.gc_max, c.max_run_length, c.reserved)

    if params.choice_mechanism == "random":
        fsm = encoding.random_fsm(
            params.symbol_size,
            params.reserved_bits,
            init_state,
            rs_cons,
            params.random_seed,
        )
    elif params.choice_mechanism == "gc_tracking":
        fsm = encoding.gc_tracking_fsm(
            params.symbol_size,
            params.reserved_bits,
            init_state,
            rs_cons,
        )
    elif params.choice_mechanism == "gc_tracked_random":
        fsm = encoding.gc_tracked_random_fsm(
            params.symbol_size,
            params.reserved_bits,
            init_state,
            rs_cons,
            params.random_seed,
        )
    elif params.choice_mechanism == "similar":
        fsm = encoding.most_similar_fsm(
            params.symbol_size,
            params.reserved_bits,
            init_state,
            rs_cons,
            params.random_seed,
        )
    elif params.choice_mechanism == "different":
        fsm = encoding.most_different_fsm(
            params.symbol_size,
            params.reserved_bits,
            init_state,
            rs_cons,
            params.random_seed,
        )
    elif params.choice_mechanism == "parity":
        fsm = encoding.parity_fsm(
            params.symbol_size,
            params.reserved_bits,
            init_state,
            rs_cons,
            params.random_seed,
        )
    else:
        raise Exception("Invalid choice mechanism")

    # conf = confusion()

    dna_errors_injected = []
    dna_errors_remaining = []

    bit_errors_injected = []
    bit_errors_remaining = []

    sequence_errors = []

    dna_len = None

    if verbose:
        print(f"\nRUNNING EXPERIMENT\n")
        print(params)

    for i in range(params.repetitions):
        # Generate random sequence or use given one.
        seq = rand_bit_string(params.sequence_length)

        # Encode sequence with convolutional code.
        enc = viterbi.encode(fsm, seq)

        # Translate encoded sequence to nucleotides (analog to DNA synthesis).
        dna = encoding.bits_to_dna(enc)
        dna_len = len(dna)

        # Inject substitution errors at given rate to
        # simulate errors during synthesis, PCR, storage or sequencing.
        # num_errors = int(params.error_rate * dna_len)
        dna_err = inject_base_errors(dna, params.error_rate)

        # Convert nucleotides back to bits (analog to DNA sequencing).
        err = encoding.dna_to_bits(dna_err)

        # Decode received bits using viterbi, get the resulting sequence.
        (_, result, observed) = viterbi.decode(fsm, err)

        # The estimated DNA sequence.
        dna_cor = bits_to_dna(observed)

        # Add data to confusion matrix
        # conf += confusion(dna, dna_cor)

        # Number of errors occuring in the DNA.
        dna_error = hamming_dist(dna, dna_err)

        # Number of errors remaining after DNA sequence is corrected.
        rem_dna_error = hamming_dist(dna, dna_cor)

        # Number of errors between the encoded and received strings.
        bit_error = hamming_dist(enc, err)

        # Number of errors remaining after the received string is corrected.
        rem_bit_error = hamming_dist(enc, observed)

        # Number of errors in the decoded sequence.
        seq_error = hamming_dist(seq, result)

        dna_errors_injected.append(dna_error)
        dna_errors_remaining.append(rem_dna_error)
        bit_errors_injected.append(bit_error)
        bit_errors_remaining.append(rem_bit_error)
        sequence_errors.append(seq_error)

        if verbose:
            print(f"REPETITION {i + 1} OF {params.repetitions} RESULTS:")
            print("----------------------")
            print(f"ERRORS INJECTED INTO DNA: {dna_error}")
            print(f"RESULTANT ERRORS IN RECEIVED STRING: {bit_error}")
            print(f"ERRORS REMAINING IN DNA AFTER DECODING: {rem_dna_error}")
            print(f"ERRORS REMAINING IN STRING AFTER DECODING: {rem_bit_error}")
            print(f"ERRORS IN DECODED SEQUENCE: {seq_error}")
            print(f"===============================================================")

    avg_dna_error = mean(dna_errors_injected)
    avg_rem_dna_error = mean(dna_errors_remaining)
    avg_bit_error = mean(bit_errors_injected)
    avg_rem_bit_error = mean(bit_errors_remaining)
    avg_seq_error = mean(sequence_errors)

    dna_percent_error = avg_dna_error / dna_len
    seq_percent_error = avg_seq_error / params.sequence_length

    if verbose:
        print("AVERAGE RESULTS:")
        print("----------------------")
        print(f"AVG. ERRORS INJECTED INTO DNA: {avg_dna_error}")
        print(f"AVG. RESULTANT ERRORS IN RECEIVED STRING: {avg_bit_error}")
        print(f"AVG. ERRORS REMAINING IN DNA AFTER DECODING: {avg_rem_dna_error}")
        print(f"AVG. ERRORS REMAINING IN STRING AFTER DECODING: {avg_rem_bit_error}")
        print(f"AVG. ERRORS IN DECODED SEQUENCE: {avg_seq_error}")
        print(f"PERCENTAGE ERROR IN DNA: {dna_percent_error}")
        print(f"PERCENTAGE ERROR IN SEQUENCE: {seq_percent_error}")
        print(f"===============================================================")

    return (
        avg_dna_error,
        avg_rem_dna_error,
        avg_bit_error,
        avg_rem_bit_error,
        avg_seq_error,
        dna_percent_error,
        seq_percent_error,
        # conf,
    )


def define_experiments(
    config: Parameters,
    error_rates: list[int],
    seed: int,
) -> list[Parameters]:
    experiments = []
    # Set initial starting seed so that all experiments are repeatable.
    rn.seed(seed)

    for rate in error_rates:
        exp = config.copy()
        exp.error_rate = rate
        # Set random seed for each experiment so that each one is individually repeatable.
        exp.random_seed = rn.randrange(seed)
        experiments.append(exp)

    return experiments


def print_results(name: str, config: Parameters, x: list[float], y: list[float]):
    print("==================== EXPERIMENT RESULTS =======================")
    print(f'"{name}":' + " {")
    print(
        f'    "title": "Mechanim: {config.choice_mechanism}, {config.reserved_bits} Reserved Bits, '
        + f'Symbol Length {config.symbol_size}, {config.constraints.short_str()}",'
    )
    print(f'    "xlabel": "Input Error Rate",')
    print(f'    "ylabel": "Output Error Rate",')
    print(f'    "x": {x},'),
    print(f'    "y": {y},')
    print("}")


def run_error_range(
    name: str,
    config: Parameters,
    error_rates: list[int],
    starting_seed: int,
    iterations=10,
):
    # Set starting seed for all experiments
    rn.seed(starting_seed)

    print(
        f"Running experiments with starting seed: {starting_seed} and error range: {error_rates}"
    )
    random_seed = starting_seed
    dna_err = []
    seq_err = []

    for i in range(iterations):
        random_seed = rn.randrange(random_seed)
        experiments = define_experiments(config, error_rates, random_seed)

        print(
            f"\nRunning iteration {i + 1} out of {iterations} with random seed: {random_seed}"
        )

        for experiment in experiments:
            _, _, _, _, _, dna_percent, seq_percent = run_experiment(experiment)
            dna_err.append(dna_percent)
            seq_err.append(seq_percent)

    print_results(name, config, dna_err, seq_err)


if __name__ == "__main__":
    # seed = 1704182
    seed = 5410293095

    config = Parameters(
        symbol_size=4,
        reserved_bits=4,
        constraints=default_constraints(gc_min=0.25, gc_max=0.75),
        sequence_length=3000,
        choice_mechanism="parity",
        repetitions=3,
    )

    error_range = np.linspace(0.0005, 0.02, num=40)

    run_error_range(
        "rust/sym-4-res-4-parity-pen-seq-3000",
        config,
        error_range,
        seed,
        iterations=5,
    )

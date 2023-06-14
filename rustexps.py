import copy
import numpy as np
import random as rn
import viterbi
import encoding
from dataclasses import dataclass
from statistics import mean
from choice_mechanism import gc_tracking, gc_tracked_random, random_choice
from constraints import Constraints, default_constraints, standard_constraints
from data_types import Path
from dna_mapping import bits_to_dna, dna_to_bits
from fsm import construct_fsm_from_constraints
from utils import (
    confusion,
    gc_content,
    hamming_dist,
    inject_base_errors,
    inject_burst_errors,
    inject_deletion_errors,
    max_gc_variance,
    rand_bit_string,
)


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
    gc_window: int = 10

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
            + f"    GC Window Size: {self.gc_window}\n"
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
    elif params.choice_mechanism == "alt_parity":
        fsm = encoding.alt_parity_fsm(
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

    gc_cont = []
    gc_variance = []

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

        # Gather info about the encoded DNA sequence.
        # gc_cont.append(gc_content(dna))
        # gc_variance.append(max_gc_variance(dna, window=params.gc_window))

        # Inject substitution errors at given rate to
        # simulate errors during synthesis, PCR, storage or sequencing.
        # num_errors = int(params.error_rate * dna_len)
        # dna_err = inject_base_errors(dna, params.error_rate)
        # dna_err = inject_deletion_errors(dna, params.error_rate)
        dna_err = inject_burst_errors(dna, params.error_rate, min_burst=4, max_burst=4)

        # Convert nucleotides back to bits (analog to DNA sequencing).
        err = encoding.dna_to_bits(dna_err)

        # Decode received bits using viterbi, get the resulting sequence.
        # (_, result, observed) = viterbi.decode(fsm, err)
        (_, result, observed) = viterbi.constraint_decode(fsm, rs_cons, err)

        # The estimated DNA sequence.
        dna_cor = encoding.bits_to_dna(observed)

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
    # avg_gc_content = mean(gc_cont)
    # avg_gc_variance = mean(gc_variance)

    dna_percent_error = avg_dna_error / dna_len
    seq_percent_error = avg_seq_error / params.sequence_length

    if verbose:
        print("AVERAGE RESULTS:")
        print("----------------------")
        # print(f"AVG. GC CONTENT: {avg_gc_content}")
        # print(f"AVG. MAX GC VARIANCE: {avg_gc_variance}")
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
        0,
        0,
        # conf,
    )


def define_experiments(
    config: Parameters,
    error_rates: list[float],
    gc_windows: list[int],
    seed: int,
) -> list[Parameters]:
    experiments = []
    # Set initial starting seed so that all experiments are repeatable.
    rn.seed(seed)

    for rate in error_rates:
        for window in gc_windows:
            exp = config.copy()
            exp.error_rate = rate
            exp.gc_window = window
            # Set random seed for each experiment so that each one is individually repeatable.
            exp.random_seed = rn.randrange(seed)
            experiments.append(exp)

    return experiments


def print_results(
    name: str,
    config: Parameters,
    x: list[float],
    y: list[float],
    gc_windows: list[int],
    gc: list[float],
    gc_var: list[float],
):
    print("==================== EXPERIMENT RESULTS =======================")
    print(f'"{name}":' + " {")
    print(
        f'    "title": "Mechanism: {config.choice_mechanism}, {config.reserved_bits} Reserved Bits, '
        + f'Symbol Length {config.symbol_size}, {config.constraints.short_str()}",'
    )
    print(f'    "xlabel": "Input Error Rate",')
    print(f'    "ylabel": "Output Error Rate",')
    print(f'    "x": {x},'),
    print(f'    "y": {y},'),
    print(f'    "window": {gc_windows},')
    print(f'    "gc": {gc},'),
    print(f'    "gc_var": {gc_var},'),
    print("}")


def run_error_range(
    name: str,
    config: Parameters,
    error_rates: list[int],
    gc_windows: list[int],
    starting_seed: int,
    iterations=10,
):
    # Set starting seed for all experiments
    rn.seed(starting_seed)

    print(
        f"\nRunning experiments with starting seed: {starting_seed} and error range: {error_rates}"
    )
    random_seed = starting_seed
    dna_err = []
    seq_err = []
    gc_win = []
    gcs = []
    gc_vars = []

    for i in range(iterations):
        random_seed = rn.randrange(random_seed)
        experiments = define_experiments(config, error_rates, gc_windows, random_seed)

        print(
            f"\nRunning iteration {i + 1} out of {iterations} with random seed: {random_seed}"
        )

        for experiment in experiments:
            _, _, _, _, _, dna_percent, seq_percent, gc, gc_var = run_experiment(
                experiment
            )
            dna_err.append(dna_percent)
            seq_err.append(seq_percent)
            gc_win.append(experiment.gc_window)
            gcs.append(gc)
            gc_vars.append(gc_var)

    print_results(name, config, dna_err, seq_err, gc_win, gcs, gc_vars)


if __name__ == "__main__":
    # Randomly generated seeds.
    seeds = [
        548061814,
        155688848,
        292348927,
        403274468,
        612819644,
        943797417,
        668695445,
        900620255,
        872647061,
        345574507,
        654795644,
        707772079,
        102585517,
        784160164,
        841153880,
        610658896,
        290172510,
        547326374,
        749241474,
        571897292,
    ]
    seed_idx = 0

    seq_len = 3000
    sizes = [4]
    reserved = [4]
    mechanisms = [
        # "random",
        # "gc_tracking",
        # "gc_tracked_random",
        # "similar",
        # "different",
        # "parity",
        "alt_parity",
    ]
    error_range = np.linspace(0.0005, 0.02, num=40)
    # error_range = np.linspace(0.001, 0.01, num=10)
    # error_range = [0]

    # gc_windows = [10, 20, 30, 40, 50]
    gc_windows = [10]

    # Number of random sequences encoded/decoded to form a single data point.
    reps = 3

    # Number of iterations each configuration is repeated for.
    iters = 5

    for size in sizes:
        for res in reserved:
            for mechanism in mechanisms:
                if (mechanism == "similar" or mechanism == "different") and (
                    size != res
                ):
                    continue
                if seq_len % (size * 2 - res) != 0:
                    continue

                c = standard_constraints(size, res)

                config = Parameters(
                    symbol_size=size,
                    reserved_bits=res,
                    constraints=c,
                    sequence_length=seq_len,
                    choice_mechanism=mechanism,
                    repetitions=reps,
                )
                seed_idx += 1

                if seed_idx >= len(seeds):
                    seed_idx = 0

                seed = seeds[seed_idx]

                mech = mechanism.replace("_", "-")
                run_error_range(
                    f"cons/sym-{size}-res-{res}-{mech}-seq-{seq_len}-b-4",
                    config,
                    error_range,
                    gc_windows,
                    seed,
                    iterations=iters,
                )

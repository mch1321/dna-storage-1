import random as rn
from choice_mechanism import gc_tracking
from data_types import Path
from dna_mapping import bits_to_dna, dna_to_bits
from experiments import Parameters
from fsm import construct_fsm_from_constraints
from graphing import plot_confusion
from utils import confusion, inject_base_errors, rand_bit_string


def calc_confusion(
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

    fsm = construct_fsm_from_constraints(
        init_state, input_size, output_size, params.constraints, params.choice_mechanism
    )

    conf = confusion("", "")

    if verbose:
        print(f"\nCALCULATING CONFUSION\n")
        print(params)

    for i in range(params.repetitions):
        if verbose:
            print(f"Iteration {i + 1}")

        # Generate random sequence.
        seq = rand_bit_string(params.sequence_length)

        # Encode sequence with convolutional code.
        enc = fsm.conv(seq)

        # Translate encoded sequence to nucleotides (analog to DNA synthesis).
        dna = bits_to_dna(enc)

        dna_err = inject_base_errors(dna, params.error_rate)

        # Convert nucleotides back to bits (analog to DNA sequencing).
        err = dna_to_bits(dna_err)

        # Decode received bits using viterbi.
        path: Path = fsm.viterbi(err)

        # The path estimated my Viterbi.
        observed = path.observations

        # The estimated correct DNA sequence.
        dna_cor = bits_to_dna(observed)

        # Add data to confusion matrix
        c = confusion(dna, dna_cor)
        if verbose:
            print("Confusion:")
            print(c)

        conf += c

    if verbose:
        print("Accumulative Confusion:")
        print(conf)

    return conf


if __name__ == "__main__":
    for er in [0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]:
        params = Parameters(
            sequence_length=300,
            choice_mechanism=gc_tracking,
            error_rate=er,
            repetitions=10,
            random_seed=1704182,
        )
        conf = calc_confusion(params, verbose=True)
        str_er = str(er).replace(".", "")
        plot_confusion(
            f"er{str_er}-seq300-rep10-gc-tracking",
            f"GC Tracking, Error Rate {er}, Symbol Length 4, 5 Reserved Bits, 0.35 < GC < 0.65",
            conf,
        )

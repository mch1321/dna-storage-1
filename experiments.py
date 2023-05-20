from dataclasses import dataclass
from statistics import mean
import random as rn
from choice_mechanism import random_choice
from constraints import Constraints, default_constraints
from data_types import Path
from dna_mapping import bits_to_dna, dna_to_bits
from fsm import construct_fsm_from_constraints
from utils import hamming_dist, inject_base_errors_exact, rand_bit_string


@dataclass
class Parameters:
    symbol_size: int = 4
    reserved_bits: int = 5
    choice_mechanism: callable = random_choice
    constraints: Constraints = default_constraints()
    sequence: str = None
    sequence_length: int = 60
    error_rate: float = 0.05
    repetitions: int = 20
    random_seed: int = None

    def __str__(self):
        return (
            "Parameters:\n"
            + f"    Symbol size: {self.symbol_size}\n"
            + f"    Reserved bits: {self.reserved_bits}\n"
            + f"    Choice mechanism: random\n"
            + f"    Constraints: default\n"
            + (
                f"    Sequence: {self.sequence}\n"
                if self.sequence is not None
                else f"    Sequence length: {self.sequence_length}\n"
            )
            + f"    Error rate: {self.error_rate}\n"
            + f"    Repetitions: {self.repetitions}\n"
            + f"    Random seed: {self.random_seed}\n"
        )


def run_experiment(
    params: Parameters = Parameters(),
    verbose: bool = False,
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

    dna_errors_injected = []
    dna_errors_remaining = []

    bit_errors_injected = []
    bit_errors_remaining = []

    sequence_errors = []

    seq_len = None
    dna_len = None

    if verbose:
        print(f"\nRUNNING EXPERIMENT\n")
        print(params)

    for i in range(params.repetitions):
        # Generate random sequence or use given one.
        seq = (
            rand_bit_string(params.sequence_length)
            if params.sequence is None
            else params.sequence
        )
        seq_len = len(seq)

        # Encode sequence with convolutional code.
        enc = fsm.conv(seq)

        # Translate encoded sequence to nucleotides (analog to DNA synthesis).
        dna = bits_to_dna(enc)
        dna_len = len(dna)

        # Inject substitution errors at given rate to
        # simulate errors during synthesis, PCR, storage or sequencing.
        num_errors = int(params.error_rate * dna_len)
        dna_err = inject_base_errors_exact(dna, num_errors)

        # Convert nucleotides back to bits (analog to DNA sequencing).
        err = dna_to_bits(dna_err)

        # Decode received bits using viterbi.
        path: Path = fsm.viterbi(err)

        # The path estimated my Viterbi.
        observed = path.observations

        # The estimated correct DNA sequence.
        dna_cor = bits_to_dna(observed)

        # Estimate of the content of the original sequence.
        result = path.sequence

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
            print(f"REPETITION {i + 1} RESULTS:")
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
    seq_percent_error = avg_seq_error / seq_len

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
    )


if __name__ == "__main__":
    params = Parameters(random_seed=42)
    run_experiment(params, verbose=True)

import time
from data_types import Path
from dna_mapping import bits_to_dna, dna_to_bits
from experiments import Parameters
from fsm import construct_fsm_from_constraints
from graphing import plot
from utils import inject_base_errors, rand_bit_string


def profile(config: Parameters) -> tuple[float, float, float]:
    output_size = 2 * config.symbol_size

    if config.reserved_bits >= output_size:
        raise Exception("Too many reserved bits for given symbol size.")

    input_size = output_size - config.reserved_bits
    init_state = output_size * "0"

    total = 0.0

    print("=======================================================")
    print("Running profiler")
    print(
        f"Sequence length {config.sequence_length}, Symbol length: {config.symbol_size}"
    )

    start_time = time.time()
    fsm = construct_fsm_from_constraints(
        init_state, input_size, output_size, config.constraints, config.choice_mechanism
    )
    fsm_duration = time.time() - start_time
    total += fsm_duration
    print(f"--- Constructing the FSM took {fsm_duration} seconds. ---")

    seq = rand_bit_string(config.sequence_length)

    start_time = time.time()
    enc = fsm.conv(seq)
    dna = bits_to_dna(enc)
    enc_duration = time.time() - start_time
    total += enc_duration
    print(f"--- Encoding the sequence took {enc_duration} seconds. ---")

    dna_err = inject_base_errors(dna, config.error_rate)

    start_time = time.time()
    err = dna_to_bits(dna_err)
    path: Path = fsm.viterbi(err)
    dec_duration = time.time() - start_time
    total += dec_duration
    print(f"--- Decoding the sequence took {dec_duration} seconds. ---")
    print(f"--- Total duration was {total} seconds. ---")

    return fsm_duration, enc_duration, dec_duration, total


if __name__ == "__main__":
    sequence_lengths = list(range(30, 360, 30))
    sequence_lengths.extend(range(360, 720, 90))
    sequence_lengths.extend(range(720, 1300, 180))
    fsm_dur = []
    enc_dur = []
    dec_dur = []
    tot_dur = []

    for length in sequence_lengths:
        fsm, enc, dec, tot = profile(Parameters(sequence_length=length))
        fsm_dur.append(fsm)
        enc_dur.append(enc)
        dec_dur.append(dec)
        tot_dur.append(tot)

    print("===================== RESULTS =======================")
    print(f"SEQUENCE LENGTHS : {sequence_lengths}")
    print(f"FSM DURATION   : {fsm_dur}")
    print(f"ENC DURATION   : {enc_dur}")
    print(f"DEC DURATION   : {dec_dur}")
    print(f"TOTAL DURATION : {tot_dur}")

    plot(
        "python-fsm-profile",
        sequence_lengths,
        fsm_dur,
        "Sequence Length / bits",
        "Duration / seconds",
        "FSM Construction Profile (Python)",
        fit=False,
    )
    plot(
        "python-enc-profile",
        sequence_lengths,
        enc_dur,
        "Sequence Length / bits",
        "Duration / seconds",
        "Encoding Profile (Python)",
        fit=False,
    )
    plot(
        "python-dec-profile",
        sequence_lengths,
        dec_dur,
        "Sequence Length / bits",
        "Duration / seconds",
        "Decoding Profile (Python)",
        fit=False,
    )
    plot(
        "python-tot-profile",
        sequence_lengths,
        tot_dur,
        "Sequence Length / bits",
        "Duration / seconds",
        "Total Profile (Python)",
        fit=False,
    )

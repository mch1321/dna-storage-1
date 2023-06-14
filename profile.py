from experiments import Parameters
from graphing import multiplot
from python_profile import profile as pyprof
from rust_profile import profile as rsprof

if __name__ == "__main__":
    sequence_lengths = list(range(30, 360, 30))
    sequence_lengths.extend(range(360, 720, 90))
    sequence_lengths.extend(range(720, 1300, 180))

    symbol_sizes = list(range(2, 21))

    fsm_dur = [[], []]
    enc_dur = [[], []]
    dec_dur = [[], []]
    tot_dur = [[], []]

    # for length in sequence_lengths:
    #     _, enc, dec, tot = pyprof(Parameters(sequence_length=length))
    #     enc_dur[0].append(enc)
    #     dec_dur[0].append(dec)
    #     tot_dur[0].append(tot)

    #     _, enc, dec, tot = rsprof(Parameters(sequence_length=length))
    #     enc_dur[1].append(enc)
    #     dec_dur[1].append(dec)
    #     tot_dur[1].append(tot)

    for length in symbol_sizes:
        fsm, _, _, _ = pyprof(Parameters(sequence_length=length), fsm_only=True)
        fsm_dur[0].append(fsm)

        fsm, _, _, _ = rsprof(Parameters(sequence_length=length), fsm_only=True)
        fsm_dur[1].append(fsm)

    labels = ["Native Python", "Rust Call"]

    multiplot(
        "profiling/pyrs-fsm",
        [symbol_sizes] * 2,
        fsm_dur,
        labels,
        "Symbol Length / Nucleotides",
        "Duration / Seconds",
        "",
        fit=False,
    )

    # multiplot(
    #     "profiling/pyrs-enc",
    #     [sequence_lengths] * 2,
    #     enc_dur,
    #     labels,
    #     "Sequence Length / Bits",
    #     "Duration / Seconds",
    #     "",
    #     fit=False,
    # )

    # multiplot(
    #     "profiling/pyrs-dec",
    #     [sequence_lengths] * 2,
    #     dec_dur,
    #     labels,
    #     "Sequence Length / Bits",
    #     "Duration / Seconds",
    #     "",
    #     fit=False,
    # )

    # multiplot(
    #     "profiling/pyrs-tot",
    #     [sequence_lengths] * 2,
    #     tot_dur,
    #     labels,
    #     "Sequence Length / Bits",
    #     "Duration / Seconds",
    #     "",
    #     fit=False,
    # )

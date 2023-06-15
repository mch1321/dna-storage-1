import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from plots import plots


def multiplot(
    name: str,
    xs: list[list],
    ys: list[list],
    set_labels: list[str],
    xlabel: str,
    ylabel: str,
    title: str,
    fit: bool = True,
    invertx: bool = False,
):
    plt.rcParams["font.size"] = 32
    fig, ax = plt.subplots(figsize=(30, 20))

    assert len(xs) <= 9
    assert len(xs) == len(ys)
    assert len(xs) == len(set_labels)

    cs = [
        "red",
        "green",
        "blue",
        "orange",
        "purple",
        "black",
        "yellow",
        "teal",
        "brown",
    ]

    for i, (x, y, l) in enumerate(zip(xs, ys, set_labels)):
        plt.scatter(x, y, s=70, c=cs[i], label=l)
        if fit:
            sn.regplot(
                x=x,
                y=y,
                ci=True,
                scatter_kws={"color": cs[i]},
                line_kws={"color": cs[i]},
            )

    ax.set(
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )

    if invertx:
        plt.legend(loc="upper right")
        ax.invert_xaxis()
    else:
        plt.legend(loc="upper left")

    file_name = name if fit else f"{name}-no-trend"
    fig.savefig(f"plots/{file_name}.png")
    plt.show()


def multiplot_from_dict(key: str, fit: bool = True):
    p = plots[key]
    multiplot(
        key,
        p["xs"],
        p["ys"],
        p["labels"],
        p["xlabel"],
        p["ylabel"],
        p["title"],
        fit,
        True,
    )


def plot(
    name: str,
    x: list,
    y: list,
    xlabel: str,
    ylabel: str,
    title: str,
    fit: bool = True,
    invertx: bool = False,
):
    plt.rcParams["font.size"] = 32
    fig, ax = plt.subplots(figsize=(30, 20))

    plt.scatter(x, y, s=70)

    ax.set(
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )

    if invertx:
        ax.invert_xaxis()

    if fit:
        sn.regplot(x=x, y=y, ci=False, line_kws={"color": "red"})

    fig.savefig(f"plots/{name}.png")
    plt.show()


def plot_from_dict(key: str, fit: bool = True):
    p = plots[key]
    plot(
        key,
        p["x"],
        p["y"],
        p["xlabel"],
        p["ylabel"],
        p["title"],
        fit,
        True,
    )


def plot_confusion(name: str, title: str, matrix: np.ndarray):
    axes = ["A", "C", "G", "T"]
    df = pd.DataFrame(matrix, axes, axes)
    df.index.name = "True Base"
    df.columns.name = "Predicted Base"
    fig = plt.figure(figsize=(14, 8))
    plt.title(title, fontsize=16)
    sn.set(font_scale=1.4)
    ax = sn.heatmap(df, annot=True, annot_kws={"size": 16}, fmt="d", linewidth=0.5)
    fig.savefig(f"plots/confusion/{name}.png")
    plt.show()


if __name__ == "__main__":
    plt.rcParams["font.size"] = 30
    # multiplot_from_dict("multiplot-reserved-bits-gc-tracking")
    # plot_from_dict("del/sym-4-res-4-random-seq-120")
    # key = "gc/sym-4-res-5-random-seq-3000"
    # p = plots[key]
    # plot(
    #     key,
    #     x=p["window"],
    #     y=p["gc_var"],
    #     xlabel="Window Size",
    #     ylabel="Maximum GC Variance",
    #     title="GC Variance: Random Choice, 5 Reserved Bits, Symbol Length 4",
    # )

    xs = [
        # plots["strs/unencoded"]["str_lens"],
        # plots["strs/sym-3-res-3-random-seq-3000"]["str_lens"],
        # plots["strs/sym-4-res-3-random-seq-3000"]["str_lens"],
        # plots["strs/sym-4-res-4-random-seq-3000"]["str_lens"],
        # plots["strs/sym-4-res-5-random-seq-3000"]["str_lens"],
        # plots["strs/sym-5-res-5-random-seq-3000"]["str_lens"],
        # plots["strs/sym-4-res-4-alt-parity-seq-3000"]["str_lens"],
        # plots["final/sym-4-res-3-random-seq-3000"]["x"],
        # plots["eval/one-half-seq-3000"]["x"],
        # plots["eval/sym-1-res-1-random-seq-3000-no-con"]["x"],
        # plots["eval/sym-2-res-2-random-seq-3000-no-con"]["x"],
        # plots["eval/sym-3-res-3-random-seq-3000-no-con"]["x"],
        # plots["eval/sym-4-res-4-random-seq-3000-no-con"]["x"],
        # plots["final/sym-4-res-4-random-seq-3000"]["x"],
        # plots["final/sym-4-res-5-random-seq-3000"]["x"],
        # plots["final/sym-4-res-3-gc-tracking-seq-3000"]["x"],
        # plots["final/sym-4-res-4-gc-tracking-seq-3000"]["x"],
        # plots["final/sym-4-res-5-gc-tracking-seq-3000"]["x"],
        # plots["final/sym-4-res-3-gc-tracked-random-seq-3000"]["x"],
        # plots["final/sym-4-res-4-gc-tracked-random-seq-3000"]["x"],
        # plots["final/sym-4-res-5-gc-tracked-random-seq-3000"]["x"],
        plots["final/sym-4-res-4-random-seq-3000"]["x"],
        plots["final/sym-4-res-4-gc-tracking-seq-3000"]["x"],
        plots["final/sym-4-res-4-gc-tracked-random-seq-3000"]["x"],
        plots["final/sym-4-res-4-similar-seq-3000"]["x"],
        plots["final/sym-4-res-4-different-seq-3000"]["x"],
        plots["final/sym-4-res-4-alt-parity-seq-3000"]["x"],
        # plots["final/sym-4-res-4-random-seq-3000"]["x"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-1"]["x"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-2"]["x"],
        # # plots["burst/sym-4-res-4-random-seq-3000-b-3"]["x"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-4"]["x"],
        # plots["burst/sym-4-res-4-alt-parity-seq-3000-b-4"]["x"],
        # plots["cons/sym-4-res-4-alt-parity-seq-3000-b-4"]["x"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-5"]["x"],
        # plots["final/sym-5-res-4-random-seq-3000"]["x"],
        # plots["final/sym-5-res-5-random-seq-3000"]["x"],
        # plots["final/sym-4-res-4-random-seq-3000"]["x"],
        # plots["final/sym-4-res-5-random-seq-3000"]["x"],
        # plots["final/sym-4-res-4-gc-tracking-seq-3000"]["x"],
        # plots["final/sym-4-res-3-gc-tracking-seq-3000"]["x"],
        # plots["final/sym-4-res-5-gc-tracking-seq-3000"]["x"],
        # plots["final/sym-4-res-5-gc-tracked-random-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-gc-tracking-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-gc-tracked-random-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-similar-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-different-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-parity-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-alt-parity-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-alt-parity-pen-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-parity-dec-seq-3000"]["x"],
        # plots["rust/sym-4-res-4-parity-pen-seq-3000"]["x"],
    ]
    ys = [
        # plots["strs/unencoded"]["strs"],
        # plots["strs/sym-3-res-3-random-seq-3000"]["strs"],
        # plots["strs/sym-4-res-3-random-seq-3000"]["strs"],
        # plots["strs/sym-4-res-4-random-seq-3000"]["strs"],
        # plots["strs/sym-4-res-5-random-seq-3000"]["strs"],
        # plots["strs/sym-5-res-5-random-seq-3000"]["strs"],
        # plots["strs/sym-4-res-4-alt-parity-seq-3000"]["strs"],
        # plots["final/sym-4-res-3-random-seq-3000"]["y"],
        # plots["eval/one-half-seq-3000"]["y"],
        # plots["eval/sym-1-res-1-random-seq-3000-no-con"]["y"],
        # plots["eval/sym-2-res-2-random-seq-3000-no-con"]["y"],
        # plots["eval/sym-3-res-3-random-seq-3000-no-con"]["y"],
        # plots["eval/sym-4-res-4-random-seq-3000-no-con"]["y"],
        plots["final/sym-4-res-4-random-seq-3000"]["y"],
        plots["final/sym-4-res-4-gc-tracking-seq-3000"]["y"],
        plots["final/sym-4-res-4-gc-tracked-random-seq-3000"]["y"],
        plots["final/sym-4-res-4-similar-seq-3000"]["y"],
        plots["final/sym-4-res-4-different-seq-3000"]["y"],
        plots["final/sym-4-res-4-alt-parity-seq-3000"]["y"],
        # plots["final/sym-4-res-5-random-seq-3000"]["y"],
        # plots["final/sym-4-res-3-gc-tracking-seq-3000"]["y"],
        # plots["final/sym-4-res-4-gc-tracking-seq-3000"]["y"],
        # plots["final/sym-4-res-5-gc-tracking-seq-3000"]["y"],
        # plots["final/sym-4-res-3-gc-tracked-random-seq-3000"]["y"],
        # plots["final/sym-4-res-4-gc-tracked-random-seq-3000"]["y"],
        # plots["final/sym-4-res-5-gc-tracked-random-seq-3000"]["y"],
        # plots["burst/sym-4-res-4-random-seq-3000"]["y"],
        # plots["final/sym-4-res-4-random-seq-3000"]["y"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-1"]["y"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-2"]["y"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-3"]["y"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-4"]["y"],
        # plots["burst/sym-4-res-4-alt-parity-seq-3000-b-4"]["y"],
        # plots["cons/sym-4-res-4-alt-parity-seq-3000-b-4"]["y"],
        # plots["burst/sym-4-res-4-random-seq-3000-b-5"]["y"],
        # plots["final/sym-5-res-4-random-seq-3000"]["y"],
        # plots["final/sym-5-res-5-random-seq-3000"]["y"],
        # plots["final/sym-4-res-4-random-seq-3000"]["y"],
        # plots["final/sym-4-res-5-random-seq-3000"]["y"],
        # plots["final/sym-4-res-3-gc-tracking-seq-3000"]["y"],
        # plots["final/sym-4-res-4-gc-tracking-seq-3000"]["y"],
        # plots["final/sym-4-res-5-gc-tracking-seq-3000"]["y"],
        # plots["final/sym-4-res-5-gc-tracked-random-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-gc-tracking-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-gc-tracked-random-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-similar-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-different-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-parity-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-alt-parity-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-alt-parity-pen-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-parity-dec-seq-3000"]["y"],
        # plots["rust/sym-4-res-4-parity-pen-seq-3000"]["y"],
    ]
    multiplot(
        name="final/sym-4-res-4-all-mech-seq-3000",
        xs=xs,
        ys=ys,
        set_labels=[
            # "Unencoded",
            # "Symbol Size 3, 3 Reserved Bits",
            # "Symbol Size 4, 3 Reserved Bits",
            # "Symbol Size 4, 4 Reserved Bits",
            # "Symbol Size 4, 5 Reserved Bits",
            # "Symbol Size 5, 5 Reserved Bits",
            # "Symbol Size 4, 4 Reserved Bits, Alt Parity"
            # "1/2 Convolutional Code",
            # "Symbol Size 1, 1 Reserved Bit, No Constraints",
            # "Symbol Size 2, 2 Reserved Bit, No Constraints",
            # "Symbol Size 3, 3 Reserved Bit, No Constraints",
            # "Symbol Size 4, 4 Reserved Bit, No Constraints",
            # "Symbol Size 4, 4 Reserved Bit, Default Constraints",
            # "Random Choice, 3 Reserved Bits",
            # "Random Choice, 4 Reserved Bits",
            # "Random Choice, 5 Reserved Bits",
            # "GC-Tracking, 3 Reserved Bits",
            # "GC-Tracking, 4 Reserved Bits",
            # "GC-Tracking, 5 Reserved Bits",
            # "Randomised GC-Tracking, 3 Reserved Bits",
            # "Randomised GC-Tracking, 4 Reserved Bits",
            # "Randomised GC-Tracking, 5 Reserved Bits",
            # "Normal",
            # "Symbol Length 5, 4 Reserved Bits",
            # "Symbol Length 5, 5 Reserved Bits",
            "Random",
            "GC Tracking",
            "Randomised GC Tracking",
            "Most Similar",
            "Most Different",
            # "Parity",
            "Alternating Parity",
            # "Alternating Parity Penalty",
            # "Parity Decoding",
            # "Parity Penalty",
        ],
        xlabel="Input Error Rate",
        ylabel="Output Error Rate",
        title="Default Constraints",
        fit=True,
        invertx=True,
    )

    # plot_confusion(
    #     name="er001-seq300-rep10-default",
    #     title="Error Rate 0.01, Symbol Length 4, 5 Reserved Bits, 0.35 < GC < 0.65",
    #     matrix=np.array(
    #         [
    #             [960, 0, 0, 0],
    #             [0, 1037, 0, 0],
    #             [0, 0, 990, 0],
    #           rust/sym-4-res-5-random"  [0, 0, 0, 1013],
    #         ]
    #     ),
    # )

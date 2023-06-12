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
        plt.scatter(x, y, s=40, c=cs[i], label=l)
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

    plt.legend(loc="upper right")

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
    fig, ax = plt.subplots(figsize=(30, 20))

    plt.scatter(x, y)

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
    # plot_from_dict("final/sym-5-res-5-random-seq-3000")
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
        # plots["gc/sym-4-res-3-random-seq-3000"]["window"],
        # plots["gc/sym-4-res-4-random-seq-3000"]["window"],
        # plots["gc/sym-4-res-5-random-seq-3000"]["window"],
        plots["gc/sym-4-res-3-gc-tracking-seq-3000"]["window"],
        plots["gc/sym-4-res-4-gc-tracking-seq-3000"]["window"],
        plots["gc/sym-4-res-5-gc-tracking-seq-3000"]["window"],
        # plots["gc/sym-4-res-3-random-seq-3000"]["window"],
        # plots["gc/sym-4-res-3-gc-tracking-seq-3000"]["window"],
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
        # plots["gc/sym-4-res-3-random-seq-3000"]["gc_var"],
        # plots["gc/sym-4-res-4-random-seq-3000"]["gc_var"],
        # plots["gc/sym-4-res-5-random-seq-3000"]["gc_var"],
        plots["gc/sym-4-res-3-gc-tracking-seq-3000"]["gc_var"],
        plots["gc/sym-4-res-4-gc-tracking-seq-3000"]["gc_var"],
        plots["gc/sym-4-res-5-gc-tracking-seq-3000"]["gc_var"],
        # plots["gc/sym-4-res-3-random-seq-3000"]["gc_var"],
        # plots["gc/sym-4-res-3-gc-tracking-seq-3000"]["gc_var"],
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
        name="gc/sym-4-res-3-5-gc-tracking-seq-3000",
        xs=xs,
        ys=ys,
        set_labels=[
            # "Random Choice, 3 Reserved Bits",
            # "Random Choice, 4 Reserved Bits",
            # "Random Choice, 5 Reserved Bits",
            "GC-Tracking, 3 Reserved Bits",
            "GC-Tracking, 4 Reserved Bits",
            "GC-Tracking, 5 Reserved Bits",
            # "Randomised GC-Tracking",
            # "GC Tracking",
            # "GC Tracked Random",
            # "Most Similar",
            # "Most Different",
            # "Parity",
            # "Alternating Parity",
            # "Alternating Parity Penalty",
            # "Parity Decoding",
            # "Parity Penalty",
        ],
        xlabel="Window Size",
        ylabel="Maximum GC Variance",
        title="",
        fit=True,
        invertx=False,
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

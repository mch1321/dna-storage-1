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
    fig, ax = plt.subplots(figsize=(12, 12))

    assert len(xs) <= 5
    assert len(xs) == len(ys)
    assert len(xs) == len(set_labels)

    cs = ["red", "green", "blue", "orange", "purple"]

    for i, (x, y, l) in enumerate(zip(xs, ys, set_labels)):
        plt.scatter(x, y, c=cs[i], label=l)
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
    fig, ax = plt.subplots(figsize=(12, 8))

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
    # multiplot_from_dict("multiplot-reserved-bits-gc-tracking")
    plot_from_dict("sym-5-res-5-gc-tracked-random")

    # plot_confusion(
    #     name="er001-seq300-rep10-default",
    #     title="Error Rate 0.01, Symbol Length 4, 5 Reserved Bits, 0.35 < GC < 0.65",
    #     matrix=np.array(
    #         [
    #             [960, 0, 0, 0],
    #             [0, 1037, 0, 0],
    #             [0, 0, 990, 0],
    #             [0, 0, 0, 1013],
    #         ]
    #     ),
    # )

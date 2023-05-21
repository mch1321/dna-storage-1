import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from plots import plots


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
    fig = plt.figure(figsize=(12, 8))
    plt.title(title, fontsize=16)
    sn.set(font_scale=1.4)
    ax = sn.heatmap(df, annot=True, annot_kws={"size": 16}, fmt="d", linewidth=0.5)
    fig.savefig(f"plots/confusion/{name}.png")
    plt.show()


if __name__ == "__main__":
    # plot_from_dict("larger-gc-tracked-random")

    plot_confusion(
        name="er001-seq300-rep10-default",
        title="Error Rate 0.01, Symbol Length 4, 5 Reserved Bits, 0.35 < GC < 0.65",
        matrix=np.array(
            [
                [960, 0, 0, 0],
                [0, 1037, 0, 0],
                [0, 0, 990, 0],
                [0, 0, 0, 1013],
            ]
        ),
    )

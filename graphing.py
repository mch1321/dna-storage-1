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


def confusion(name: str, matrix: list[list[int]]):
    axes = ["A", "C", "G", "T"]
    df_cm = pd.DataFrame(matrix, axes, axes)
    fig = plt.figure(figsize=(12, 8))
    sn.set(font_scale=1.4)
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16})
    fig.savefig(f"plots/confusion/{name}.png")
    plt.show()


if __name__ == "__main__":
    # plot_from_dict("larger-gc-tracking")

    confusion(
        name="eg",
        matrix=[
            [13, 1, 1, 0],
            [3, 9, 6, 0],
            [0, 0, 16, 2],
            [0, 1, 0, 15],
        ],
    )

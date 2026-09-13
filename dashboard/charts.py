import matplotlib.pyplot as plt


def model_comparison_chart(results):

    fig, ax = plt.subplots()

    ax.bar(
        results["Model"],
        results["RMSE"]
    )

    ax.set_title(
        "Model RMSE Comparison"
    )

    ax.set_ylabel("RMSE")

    ax.tick_params(
        axis="x",
        rotation=45
    )

    fig.tight_layout()

    return fig
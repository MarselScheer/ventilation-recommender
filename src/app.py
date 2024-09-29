import json
from shiny.express import render, input, ui


def load_data() -> list:
    """
    Load data from `data/meas.jsonl`

    :return: list of dicts with fields tiemstamp, humidity, temperature
    """
    rtn = []
    with open("data/meas.jsonl", "r") as f:
        for line in f:
            rtn.append(json.loads(line))
    return rtn


@render.plot
def humidity_plot():
    """
    Creates a plot of humidity and temperature over time (last 30 minutes)
    """
    from datetime import datetime
    from matplotlib import pyplot as plt

    data = load_data()[-30:]
    x = [datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S.%f") for e in data]
    h = [e["humidity"] for e in data]
    t = [e["temperature"] for e in data]

    fig, ax1 = plt.subplots()

    color = "tab:blue"
    ax1.set_xlabel("time")
    ax1.set_ylabel("humidity", color=color)
    ax1.plot(x, h, color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

    color = "tab:red"
    ax2.set_ylabel("temp", color=color)  # we already handled the x-label with ax1
    ax2.plot(x, t, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    return fig

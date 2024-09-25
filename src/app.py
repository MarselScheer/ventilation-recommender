import json
from shiny.express import render, input, ui

ui.input_slider("val", "Slider label", min=0, max=100, value=50)


def load_data() -> list:
    rtn = []
    with open("data/meas.jsonl", "r") as f:
        for line in f:
            rtn.append(json.loads(line))
    return rtn


@render.plot
def humidity_plot():
    from matplotlib import pyplot as plt

    data = load_data()
    y = [e["humidity"] for e in data]
    fig = plt.plot(range(len(y)), y)
    return fig


@render.text
def slider_val():
    return f"Slider value: {input.val()}"

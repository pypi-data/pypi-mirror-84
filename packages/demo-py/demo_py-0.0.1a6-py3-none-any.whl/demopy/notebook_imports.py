import textwrap
import collections
import io
import itertools
import json
import uuid
from typing import Any, AnyStr, Mapping, NamedTuple, Optional

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.core.display import HTML, display
from IPython.display import (JSON, SVG, Image, Javascript, Markdown, Pretty,
                             display_html, display_javascript)
from IPython.display import JSON, display_json, Code

# https://www.datacamp.com/community/tutorials/wordcloud-python


def debug(x):
    print(x)
    return x



highlight_css = {
    "background-color": "yellow", 
    "opacity": "0.75"
}

def construct_column_highlighting_function(column_name, css):
    '''
    highlight the maximum in a Series yellow.
    '''
    css = "; ".join([f"{k}: {v}" for k, v in css.items()])
    def inner(column_of_data):
        return [
            css if column_of_data.name == column_name else ''
            for x in np.arange(len(column_of_data))
        ]
    return inner


def highlight_columns(df, *columns, css=highlight_css):
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Building-Styles-Summary
    # Column wise ...
    if len(columns) < 1:
        return df.style

    return highlight_columns(df, *columns[:-1], css=css).apply(
        construct_column_highlighting_function(columns[-1], css),
        axis=0
    )
    

def extract_figure_as_image(w, h) -> widgets.Image :
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)
    img = widgets.Image(
        value=image.read(),
        format='png',
        width=w,
        height=h
    )
    img.layout.margin = "0 0 0 0"
    return img

def bar_chart(values: dict, title="Chart", yaxis="y", xaxis="x", width_factor=35, height_factor=15, str_width=5):
    # print(values)
    # https://stackoverflow.com/questions/8598673/how-to-save-a-pylab-figure-into-in-memory-file-which-can-be-read-into-pil-image
    fig = plt.figure(figsize=(width_factor, height_factor))
    # TODO - instead of using textwrap, tilt them
    x = ["\n".join(textwrap.wrap(i, width=5)) for i in list(values.keys())]
    bar_num = np.arange(len(x))
    y = list(values.values())
    plt.bar(bar_num, y, alpha=0.5, align='center', width=0.5)
    plt.xticks(bar_num, x)
    # plt.ylabel(yaxis)
    # plt.xlabel(xaxis)
    # plt.title(title)
    # plt.show(fig)
    img = extract_figure_as_image(100*width_factor, 100*height_factor)
    plt.close(fig)
    return img
    


def button(text):
    return widgets.Checkbox(
        value=False,
        description=text,
        disabled=False
    )


def container(stuff):
    return widgets.VBox(stuff)


def to_output(content, display_function=display):
    """
    returns how ipython displays content by default
    """
    x = widgets.Output()
    with x:
        display_function(content)
    return x

def tab_with_content(content_dict, key_order=lambda l: l):
    """
    Creates a tab with dicts where keys are tabnames and content are the content of the tab ...
    """
    tab = widgets.Tab()
    keys = key_order(list(content_dict.keys()))
    tab.children = [content_dict[k] for k in keys]
    for (i,title) in enumerate(keys):
        tab.set_title(i, title)
    return tab


def set_id_for_dom_element_of_output_for_current_cell(_id):
    display(Javascript('console.log(element.get(0)); element.get(0).id = "{}";'.format(_id)))


def json_code(j):
    return Code(data=json.dumps(j, indent=4), language="json")


class InteractiveJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        elif isinstance(json_data, JSON):
            self.json_str = json_data.data
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid),
            raw=True
        )
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
          renderjson.set_icons('+', '-');
          renderjson.set_show_to_level("2");
          document.getElementById('%s').appendChild(renderjson(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)


def plot_pie(d):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    keys = [x for x in d.keys()]
    values = [x for x in d.values()]
    labels = [f"{d[k]*100:2.1f}%: {k}" for k in keys]
    # labels = [f"{d[k]['value']*100:2.1f}%: {k}" for k in keys]
    sizes = np.asarray(values, np.float32)
    # sizes = [v["value"] for v in values]
    if sizes.sum() >= 1.0:
        # sizes = np.asarray([x - (16.0 * e) for x in sizes], np.float32)
        sizes = sizes - np.finfo(np.float32).eps
    # print(sizes, sum(sizes), sizes.sum(), labels)
    fig1, ax1 = plt.subplots(figsize=(12.5, 7.5))
    ax1.pie(sizes, labels=None, shadow=True, startangle=90, normalize=False)
    # ax1.pie(sizes, labels=None, autopct='%1.1f%%', shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(labels, loc="lower right", prop={'size': 10})
    image = extract_figure_as_image(1250, 750)
    plt.tight_layout()
    plt.close(fig1)
    return image


def string_to_md_list(s):
    return Markdown("\n".join([
        f"* {x}"
        for x in s.split('.')
        if x
    ]))

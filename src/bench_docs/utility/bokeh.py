import urllib.request
from enum import Enum
from typing import List

import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, Legend

from bench_docs.dataframe import Columns


def download_bokeh_scripts(version, location):
    urls = [
        f"https://cdn.bokeh.org/bokeh/release/bokeh-{version}.min.js",
        f"https://cdn.bokeh.org/bokeh/release/bokeh-widgets-{version}.min.js",
        f"https://cdn.bokeh.org/bokeh/release/bokeh-tables-{version}.min.js"
    ]

    filenames = []

    for url in urls:
        filename = url.split("/")[-1]
        filenames.append(filename)
        filepath = f"{location}/{filename}"
        urllib.request.urlretrieve(url, filepath)

    return filenames


class Tools(Enum):
    CROSSHAIR = "crosshair"
    PAN = "pan"
    WHEEL_ZOOM = "wheel_zoom"
    BOX_ZOOM = "box_zoom"
    RESET = "reset"
    HOVER = "hover"
    SAVE = "save"

    @staticmethod
    def set_tools(*tools: 'Tools') -> str:
        return ",".join([tool.value for tool in tools])

    @staticmethod
    def default_tools() -> str:
        return Tools.set_tools(Tools.CROSSHAIR, Tools.PAN, Tools.WHEEL_ZOOM, Tools.BOX_ZOOM, Tools.RESET, Tools.HOVER, Tools.SAVE)


def create_tooltips(additional_columns: List[str]) -> List[tuple[str, str]]:
    # TODO https://docs.bokeh.org/en/latest/docs/user_guide/interaction/tools.html#custom-tooltip
    tooltips = []
    for col in Columns:
        if col.source_hover_text:
            tooltips.append((col.name,  col.source_hover_text))
    for col in additional_columns:
        tooltips.append((col,  "@{" + col + "}"))
    return tooltips


def create_hover_tool(additional_columns: List[str]) -> HoverTool:
    return HoverTool(
        tooltips=create_tooltips(additional_columns),
        formatters={
            "@{" + Columns.DATETIME.name + "}": 'datetime',
        },
        mode='mouse'
    )


def create_legend(items: List[tuple[str, List]]) -> Legend:
    legend = Legend(items=items, location=(0, -30))
    legend.location = "top_right"
    legend.click_policy = "hide"
    return legend


def create_data_source(df: pd.DataFrame, additional_columns: List[str]) -> ColumnDataSource:
    data = dict()
    for col in Columns:
        if isinstance(df.index, pd.MultiIndex) and col.use_as_index:
            data[col.name] = df.index.get_level_values(col.name).tolist()
        else:
            data[col.name] = df[col.name].tolist()
    for col in additional_columns:
        if isinstance(df.index, pd.MultiIndex):
            data[col] = df.index.get_level_values(col).tolist()
        else:
            data[col] = df[col].tolist()
    data["x"] = df["x"].tolist()
    return ColumnDataSource(data=data)

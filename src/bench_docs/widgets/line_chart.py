#TODO
#Add hover https://docs.bokeh.org/en/latest/docs/examples/plotting/hover.html
import random
from typing import List

import pandas as pd
from bokeh.io import curdoc
from bokeh.models import Range1d
from bokeh.palettes import Category20
from bokeh.plotting import figure

from bench_docs.dataframe import Columns, normalize_values_to, compute_x_indexes
from bench_docs.utility.bokeh import create_data_source, create_legend, Tools, create_hover_tool
from bench_docs.utility.units import reversed_factors


class LineChart:
    def __init__(self, df: pd.DataFrame, additional_columns: List[str], figure_params: dict):

        time_unit = df[Columns.TIME_UNIT.name].iloc[0]
        normalize_values_to(df, time_unit)
        x_ticks, x_ticks_label = compute_x_indexes(df)

        curdoc().theme = 'dark_minimal'
        self.palette = Category20[20]

        self.fig = figure(**figure_params, tools=Tools.default_tools())
        self.fig.add_tools(create_hover_tool(additional_columns))
        self.fig.sizing_mode = "scale_width"

        self.fig.toolbar_location = "above"

        self.fig.yaxis.axis_label = f"Real-time ({time_unit})"
        self.fig.yaxis.axis_label_text_font_style = "bold"
        self.fig.y_range.bounds = (0, None)

        self.fig.xaxis.ticker = x_ticks
        self.fig.xaxis.major_label_overrides = x_ticks_label
        self.fig.xaxis.major_label_orientation = -45
        self.fig.xaxis.axis_label = "Git Commit/Tag"
        self.fig.xaxis.axis_label_text_font_style = "bold"
        self.fig.x_range.bounds = (-0.1, None)

        groups = df.groupby([Columns.NAME.name] + additional_columns)
        legends = []
        i = 0
        circles = []
        for name, group in groups:
            source = create_data_source(group, additional_columns)
            line = self.fig.line(x="x", y=Columns.MEAN.name, source=source, line_width=4, color=self.palette[i])
            circle = self.fig.circle(x="x", y=Columns.MEAN.name, source=source, line_width=8, color=self.palette[i+1])

            circles.append(circle)
            legends.append(('_'.join(name[1:]), [circle, line]))
            i += 2

        self.fig.hover.renderers = circles
        self.fig.add_layout(create_legend(legends), 'right')

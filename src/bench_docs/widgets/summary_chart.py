from typing import List

import pandas as pd
from bokeh.io import show, curdoc
from bokeh.layouts import column, row
from bokeh.models import MultiSelect, CustomJS

from bench_docs.dataframe import Columns
from bench_docs.widgets.line_chart import LineChart


class SummaryChart:
    def __init__(self, df: pd.DataFrame, additional_columns: List[str]):
        self.height = 300
        self.multi_select = False

        plots = []
        groups = df.groupby([Columns.NAME.name])
        for name, group in groups:
            chart = LineChart(group, additional_columns, dict(title=' '.join(name), height=200))
            plots.append(chart.fig)

        layout = column(plots)
        layout.sizing_mode = "scale_width"

        if self.multi_select:
            options = [(str(i), str(group[0])) for i, group in enumerate(groups)]
            value = [str(i) for i in range(len(plots))]
            select = MultiSelect(options=options, value=value, height=self.height, width=200)

            callback = CustomJS(args=dict(plots=plots, col=layout, select=select), code="""
            const children = []
            for (const i of select.value) {
                children.push(plots[i])
            }
            col.children = children
            """)

            select.js_on_change('value', callback)

            r = row(select, layout)
            r.sizing_mode = "scale_width"
            curdoc().add_root(r)
            show(r)
        else:
            show(layout)

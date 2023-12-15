from typing import List

import pandas as pd
from bokeh.io import show, curdoc
from bokeh.layouts import column, row
from bokeh.models import Legend, MultiSelect, CustomJS
from bokeh.palettes import Category10
from bokeh.plotting import figure

from bench_docs.dataframe import Columns
from bench_docs.utility.units import reversed_factors


class SummaryChart:
    def __init__(self, df: pd.DataFrame, additional_columns: List[str]):
        self.height = 300
        self.multi_select = False


        # Create a sorted list of all git commits/tag
        git_commits = df.drop_duplicates(subset=[Columns.GIT_COMMIT.name])
        git_commits = git_commits.sort_values(by=[Columns.DATETIME.name])
        git_commits = git_commits[Columns.GIT_COMMIT.name].tolist()

        plots = []
        groups = df.groupby([Columns.NAME.name])
        for name, group in groups:
            p = figure(title=str(name), height=self.height)
            p.sizing_mode = "scale_width"
            p.yaxis.axis_label = "Real-time " + "(" + reversed_factors.get(group[Columns.TIME_UNIT.name].iloc[0]) + ")"
            p.yaxis.axis_label_text_font_style = "bold"
            p.toolbar_location = "above"

            configs = group.groupby(additional_columns)
            legends = []
            i = 0
            for config, subgroup in configs:
                x = [git_commits.index(commit) for commit in subgroup[Columns.GIT_COMMIT.name]]
                y = [mean for mean in subgroup[Columns.MEAN.name]]
                circle = p.circle(x=x, y=y, line_width=4, color=Category10[10][i % 10])
                line = p.line(x=x, y=y, line_width=2, color=Category10[10][i % 10])
                legends.append((str(config), [circle, line]))
                i += 1

            x_ticks = [i for i in range(len(git_commits))]
            x_ticks_labels = {key: value[:8] for key, value in enumerate(git_commits)}
            p.xaxis.ticker = x_ticks
            p.xaxis.major_label_overrides = x_ticks_labels
            p.xaxis.major_label_orientation = -45
            p.xaxis.axis_label = "Git Commit/Tag"
            p.xaxis.axis_label_text_font_style = "bold"

            legend = Legend(items=legends, location=(0, -30))
            legend.location = "top_right"
            legend.click_policy = "hide"
            p.add_layout(legend, 'right')
            plots.append(p)


        curdoc().theme = 'dark_minimal'
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

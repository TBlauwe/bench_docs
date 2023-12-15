import argparse
import os

import pandas as pd
from bokeh.models import Legend
from bokeh.palettes import Category10

from bench_docs.dataframe import Columns
from bench_docs.media.summary_chart import SummaryChart
from bench_docs.utility import git
from bench_docs.utility.asserts import assert_file_exists
from bench_docs.parser.google_benchmark import GoogleBenchmarkParser
from bench_docs.settings import Settings
from bench_docs.utility.dsl import retrieve_integer
from bench_docs.utility.file import retrieve_all_files_from
from bokeh.plotting import figure, show


class App:

    def __init__(self, filepath):
        assert_file_exists(filepath)
        self.settings = Settings(filepath)
        self.files = retrieve_all_files_from(self.settings.benchmarks_directory)
        self.repo = git.Repository(self.settings.git_directory)

        self.additional_columns = list(self.settings.parameters.keys())
        self.columns = [x.name for x in Columns] + self.additional_columns

        self.df = pd.DataFrame(columns=self.columns)

        for col in Columns:
            self.df[col.name] = self.df[col.name].astype(col.type)
            print(self.df[col.name])
        for col in self.additional_columns:
            self.df[col] = self.df[col].astype('string')
            print(self.df[col])

    def run(self):
        self.build_dataframe()
        self.reorganize_dataframe()
        print("Breakpoint")
        SummaryChart(self.df, self.additional_columns)
        print("Breakpoint")

    def build_dataframe(self):
        for file in self.files:
            self.repo.change_commit(file.name)
            config = {Columns.DATETIME.name: self.repo.get_datetime(), Columns.GIT_COMMIT.name: file.name}

            # Infer additional columns value
            for key, value in self.settings.parameters.items():
                if isinstance(value, str) and value.startswith("@"):
                    config[key] = file.folders[retrieve_integer(value) - 1]

            if self.settings.benchmarks_format == "GoogleBenchmark":
                GoogleBenchmarkParser.parse(self.df, self.settings, config, file)
            else:
                print(f"Error: {self.settings.benchmarks_format} is not a supported format.")

    # A multi-sort is applied by name and datetime
    def reorganize_dataframe(self):
        self.df = self.df.sort_values(by=["Name", "Datetime"])
        icols = [col.name for col in Columns if col.use_as_index] + self.additional_columns
        index = pd.MultiIndex.from_frame(self.df[icols])
        self.df.index = index
        self.df = self.df.drop(columns=icols)


def run(filepath: str):
    # Generate charts
    for title, chart in settings.charts.items():
        _df = df.query(chart.query)

        # Create a sorted list of all git commits/tag
        git_commits = _df.drop_duplicates(subset=['Git commit/tag'])
        git_commits = git_commits.sort_values(by=["Datetime"])
        git_commits = git_commits["Git commit/tag"].tolist()

        p = figure(title=os.path.splitext(title)[0], toolbar_location="above")
        p.title.text_font_style = "bold"

        p.xaxis.axis_label = "Git Commit/Tag"
        p.xaxis.axis_label_text_font_style = "bold"
        p.yaxis.axis_label = "Real-time " + "(" + _df["TimeUnit"].iloc[0] + ")"
        p.yaxis.axis_label_text_font_style = "bold"

        p.sizing_mode = "scale_width"
        groups = _df.groupby(["Name"] + additionnal_columns)

        legends = []
        i = 0

        for name, group in groups:
            x = [git_commits.index(commit) for commit in group["Git commit/tag"]]
            y = [mean for mean in group["Mean"]]
            circle = p.circle(x=x, y=y, line_width=4, color=Category10[10][i % 10])
            line = p.line(x=x, y=y, line_width=2, color=Category10[10][i % 10])
            legends.append((str(name), [circle, line]))
            i += 1

        legend = Legend(items=legends, location=(0, -30))
        legend.location = "top_right"
        legend.click_policy = "hide"
        p.add_layout(legend, 'right')

        x_ticks = [i for i in range(len(git_commits))]
        x_ticks_labels = {key: value for key, value in enumerate(git_commits)}
        p.xaxis.ticker = x_ticks
        p.xaxis.major_label_overrides = x_ticks_labels
        p.xaxis.major_label_orientation = -45

        show(p)

    print("Done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate charts from your benchmarks results.")
    parser.add_argument("filepath", default="settings.json", help="Filepath to the settings .json file")

    args = parser.parse_args()

    App(args.filepath).run()

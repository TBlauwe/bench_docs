import argparse

import pandas as pd
from bokeh.models import ColumnDataSource, Legend
from bokeh.palettes import Category10

from bench_docs.utility import git
from bench_docs.utility.asserts import assert_file_exists
from bench_docs.parser.google_benchmark import GoogleBenchmarkParser
from bench_docs.settings import Settings
from bench_docs.utility.dsl import retrieve_integer
from bench_docs.utility.file import retrieve_all_files_from
from bench_docs.utility.units import convert_time
from bokeh.plotting import figure, show

def run(filepath: str):
    assert_file_exists(filepath)

    # Setup
    settings = Settings(filepath)
    files = retrieve_all_files_from(settings.benchmarks_directory)
    repo = git.Repository(settings.git_directory)

    additionnal_columns = list(settings.parameters.keys())
    columns = ['Name', 'Datetime', 'Mean', 'Median', 'TimeUnit', 'Stddev', 'Git commit/tag'] + additionnal_columns
    icolumns = ['Name', 'Datetime', 'Git commit/tag'] + additionnal_columns
    df = pd.DataFrame(columns=columns)

    # Parse
    for file in files:
        repo.change_commit(file.name)
        config = {"Datetime": repo.get_datetime(), "Git commit/tag": file.name}
        for key, value in settings.parameters.items():
            if isinstance(value, str) and value.startswith("@"):
                config[key] = file.folders[retrieve_integer(value)-1]

        if settings.benchmarks_format == "GoogleBenchmark":
            GoogleBenchmarkParser.parse(df, settings, config, file)
        else:
            print(f"Error: {settings.benchmarks_format} is not a supported format.")

    # Reorganize dataframe
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    new_icolumns = icolumns.copy()
    new_icolumns.remove('Datetime')
    new_icolumns.remove('Git commit/tag')
    df = df.sort_values(by=["Name", "Datetime"])
    index = pd.MultiIndex.from_frame(df[new_icolumns])
    df.index = index
    df = df.drop(columns=new_icolumns)

    # Generate charts
    for title, chart in settings.charts.items():
        _df = df.query(chart.query)

        p = figure(title=title, x_axis_type='datetime', toolbar_location="above")
        groups = _df.groupby(["Name"] + additionnal_columns)

        legends = []
        i = 0

        for name, group in groups:
            source = ColumnDataSource(group)
            line = p.line(x="Datetime", y="Mean", source=source, line_width=2, color=Category10[10][i % 10])
            legends.append((str(name), [line]))
            i += 1

        legend = Legend(items=legends, location=(0, -30))
        legend.location = "top_right"
        legend.click_policy = "hide"
        p.add_layout(legend, 'right')
        show(p)

    print("Done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate charts from your benchmarks results.")
    parser.add_argument("filepath", default="settings.json", help="Filepath to the settings .json file")

    args = parser.parse_args()

    run(args.filepath)

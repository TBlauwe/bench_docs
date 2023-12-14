import argparse

import pandas as pd

from bench_docs.utility import git
from bench_docs.utility.asserts import assert_file_exists
from bench_docs.parser.google_benchmark import GoogleBenchmarkParser
from bench_docs.settings import Settings
from bench_docs.utility.dsl import retrieve_integer
from bench_docs.utility.file import retrieve_all_files_from


def run(filepath: str):
    assert_file_exists(filepath)

    # Setup
    settings = Settings(filepath)
    files = retrieve_all_files_from(settings.benchmarks_directory)
    repo = git.Repository(settings.git_directory)

    df = pd.DataFrame(columns=['Name', 'Datetime', 'Mean', 'Median', 'TimeUnit', 'Stddev', 'Git commit/tag'] + list(settings.parameters.keys()))
    df["TimeUnit"] = ""

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
    print("Done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate charts from your benchmarks results.")
    parser.add_argument("filepath", default="settings.json", help="Filepath to the settings .json file")

    args = parser.parse_args()

    run(args.filepath)

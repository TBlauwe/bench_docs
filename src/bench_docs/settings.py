import json
from bench_docs.utility import git
from bench_docs.utility.asserts import assert_file_exists, assert_directory_exists
from bench_docs.utility.file import File


class Chart:
    def __init__(self, query, include_table, include_csv):
        self.query = query
        self.include_table = include_table
        self.include_csv = include_csv


class Settings:
    def __init__(self, filename):
        assert_file_exists(filename)

        with open(filename) as f:
            data = json.load(f)
            self.benchmarks_directory = data["benchmarks_directory"]
            assert_directory_exists(self.benchmarks_directory)

            self.benchmarks_format = data["benchmarks_format"]
            self.parameters = data["parameters"]

            self.git_directory = data["git_directory"]
            assert_directory_exists(self.git_directory)

            self.charts = {}
            for key, value in data["charts"].items():
                self.charts[key] = Chart(value["query"], value["include_table"], value["include_csv"])

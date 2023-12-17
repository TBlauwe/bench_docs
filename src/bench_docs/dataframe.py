from dataclasses import dataclass
from enum import Enum
from typing import List

import pandas as pd

from bench_docs.utility.units import convert_time


@dataclass
class ColumnsData:
    name: str
    source_hover_text: str
    type: str
    use_as_index: bool


class Columns(Enum):
    NAME = ColumnsData("Name", "@Name", "string", True)
    MEAN = ColumnsData("Mean", "@Mean (@{Time unit})", "float64", False)
    MEDIAN = ColumnsData("Median", "@Median (@{Time unit})", "float64", False)
    TIME_UNIT = ColumnsData("Time unit", "", "string", False)
    STDDEV = ColumnsData("Standard deviation", "@{Standard deviation} %", "float32", False)
    GIT_COMMIT = ColumnsData("Git commit or tag", "@{Git commit or tag}", "string", False)
    DATETIME = ColumnsData("Datetime", "@{Datetime}", "datetime64[s]", False)

    @property
    def name(self):
        return self.value.name

    @property
    def type(self):
        return self.value.type

    @property
    def use_as_index(self):
        return self.value.use_as_index

    @property
    def source_hover_text(self):
        return self.value.source_hover_text


def normalize_values_to(df: pd.DataFrame, time_unit: str):
    df[Columns.MEAN.name] = df.apply(lambda row: convert_time(row[Columns.MEAN.name], row[Columns.TIME_UNIT.name], time_unit), axis=1)
    df[Columns.MEDIAN.name] = df.apply(lambda row: convert_time(row[Columns.MEDIAN.name], row[Columns.TIME_UNIT.name], time_unit), axis=1)
    df[Columns.TIME_UNIT.name] = time_unit


def compute_x_indexes(df: pd.DataFrame) -> tuple[List[int], dict]:
    git_commits = df.drop_duplicates(subset=[Columns.GIT_COMMIT.name])
    git_commits = git_commits.sort_values(by=[Columns.DATETIME.name])
    git_commits = git_commits[Columns.GIT_COMMIT.name].tolist()
    df["x"] = [git_commits.index(commit) for commit in df[Columns.GIT_COMMIT.name]]
    x_ticks = [i for i in range(len(git_commits))]
    x_ticks_label = {key: value[:8] for key, value in enumerate(git_commits)}
    return x_ticks, x_ticks_label

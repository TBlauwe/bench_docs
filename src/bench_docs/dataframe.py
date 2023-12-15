from dataclasses import dataclass
from enum import Enum

import pandas as pd


@dataclass
class ColumnsData:
    name: str
    type: str
    use_as_index: bool


class Columns(Enum):
    NAME = ColumnsData("Name", "string", True)
    MEAN = ColumnsData("Mean", "float64", False)
    MEDIAN = ColumnsData("Median", "float64", False)
    TIME_UNIT = ColumnsData("Time unit", "float64", False)
    STDDEV = ColumnsData("Standard deviation", "float32", False)
    GIT_COMMIT = ColumnsData("Git commit or tag", "string", False)
    DATETIME = ColumnsData("Datetime", "datetime64[s]", False)

    @property
    def name(self):
        return self.value.name

    @property
    def type(self):
        return self.value.type

    @property
    def use_as_index(self):
        return self.value.use_as_index


def normalize_column(df: pd.DataFrame, col_name: str, target_unit: "") -> pd.DataFrame:
    pass

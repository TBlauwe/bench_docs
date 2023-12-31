import json
import pandas as pd

from bench_docs.dataframe import Columns
from bench_docs.parser.parser import AbstractParser
from bench_docs.settings import Settings
from bench_docs.utility.file import File
from bench_docs.utility.units import factors


class GoogleBenchmarkParser(AbstractParser):
    """
    A parser class for parsing Google Benchmark JSON files.
    """
    @staticmethod
    def parse(df: pd.DataFrame, settings: Settings, config: dict, file: File):

        with open(file.abspath, 'r') as f:
            data = json.load(f)

        for b in data["benchmarks"]:
            config[Columns.NAME.name] = b['run_name']
            index = str(hash(frozenset(config.values())))

            if index not in df.index:
                df.loc[index] = config
            # Set stats and supports "aggregate" runs additional stats.
            if b['run_type'] == 'aggregate':
                if b['aggregate_name'] == 'mean':
                    df.loc[index, Columns.MEAN.name] = b.get('real_time')
                    df.loc[index, Columns.TIME_UNIT.name] = b.get('time_unit')
                elif b['aggregate_name'] == 'median':
                    df.loc[index, Columns.MEDIAN.name] = b.get('real_time')
                elif b['aggregate_name'] == 'stddev':
                    df.loc[index, Columns.STDDEV.name] = b.get('real_time')
            else:
                df.loc[index, Columns.MEAN.name] = b.get('real_time')
                df.loc[index, Columns.TIME_UNIT.name] = b.get('time_unit')

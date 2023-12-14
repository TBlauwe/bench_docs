from abc import ABC, abstractmethod
import pandas as pd
from bench_docs.utility.file import File
from bench_docs.settings import Settings


class AbstractParser(ABC):

    @staticmethod
    @abstractmethod
    def parse(df: pd.DataFrame, settings: Settings, config: dict, file: File):
        pass

import os
import pandas as pd
from pandas.errors import EmptyDataError


class Ptrms:
    def __init__(self, file, ref_start, ref_end, sample_start, sample_end):
        self.file = file
        self.ref_start = ref_start
        self.ref_end = ref_end
        self.sample_start = sample_start
        self.sample_end = sample_end
        self.frame = pd.DataFrame
        self.errors = []

    def run(self):
        self.load()
        self.extract_windows()

    def _load(self, sep, excel=False):
        if excel:
            try:
                self.frame = pd.read_excel(self.file)
            except pd.errors.EmptyDataError:
                self.seek(0)
                self._load(sep=None, excel=True)
        else:
            try:
                self.frame = pd.read_csv(self.file, sep=sep)
            except pd.errors.EmptyDataError:
                self.file.seek(0)
                self._load(sep, excel)

    def load(self):
        try:
            extension = os.path.splitext(self.file.name)[-1]
            if extension == ".txt":
                self._load(sep="\t")
            elif extension == ".csv":
                self._load(sep=",")
            elif extension in (".xlsx", ".xlsm"):
                self._load(sep=None, excel=True)
            self.frame.index = self.frame["Cycle"].apply(lambda x: int(x))
            self.frame.drop(
                columns=["AbsTime", "RelTime"], errors="ignore", inplace=True
            )
        except IndexError:
            self.errors.append("Unable to find the extension of the file.")

    def extract_windows(self):
        ref_window_stats = (
            self.frame.loc[int(self.ref_start) - 1 : int(self.ref_end)]
            .drop(columns=["Cycle"], errors="ignore")
            .describe()
        )
        sample_window_stats = (
            self.frame.loc[int(self.sample_start) - 1 : int(self.sample_end)]
            .drop(columns=["Cycle"], errors="ignore")
            .describe()
        )

        dif_stats = sample_window_stats.transpose().sub(ref_window_stats.transpose())
        out_path = os.path.join(
            os.path.dirname(self.file.name), "extracted_window.xlsx"
        )
        dif_stats.to_excel(out_path)

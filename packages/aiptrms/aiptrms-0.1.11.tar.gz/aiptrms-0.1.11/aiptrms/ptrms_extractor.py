import os
from datetime import date

import pandas as pd
from pandas.errors import EmptyDataError


class Ptrms:
    TODAY = date.today()

    def __init__(self, file, ref_start, ref_end, sample_start, sample_end, threshold):
        self.file = file
        self.ref_start = ref_start
        self.ref_end = ref_end
        self.sample_start = sample_start
        self.sample_end = sample_end
        self.frame = pd.DataFrame
        self.errors = []
        self.threshold = threshold
        self.dif = pd.DataFrame
        self.out_path = lambda x: os.path.join(os.path.dirname(self.file.name), x)

    def run(self):
        self.load()
        self.extract_windows()

    def _load(self, sep, excel=False):
        if excel:
            try:
                self.frame = pd.read_excel(self.file)
            except pd.errors.EmptyDataError:
                self.file.seek(0)
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
            self.frame.loc[int(self.ref_start) : int(self.ref_end)]
            .drop(columns=["Cycle"], errors="ignore")
            .describe()
        ).transpose()
        sample_window_stats = (
            self.frame.loc[int(self.sample_start) : int(self.sample_end)]
            .drop(columns=["Cycle"], errors="ignore")
            .describe()
        ).transpose()

        self.dif = sample_window_stats.sub(ref_window_stats)
        self.dif = self.dif.add_prefix("Difference ")
        sample_window_stats = sample_window_stats.add_prefix("Sample ")
        ref_window_stats = ref_window_stats.add_prefix("Reference ")
        self.dif = pd.concat([self.dif, sample_window_stats, ref_window_stats], axis=1)
        out_path = self.out_path(f"extracted_window_{self.TODAY}.xlsx")
        try:
            self.dif.to_excel(out_path)
        except PermissionError as e:
            self.errors.append("Unable to write window data, the file may be open")
        if self.threshold:
            self.threshold = int(self.threshold)
            self.threshold_extract()

    def threshold_extract(self):
        rows = self.dif[self.dif["Difference max"] >= self.threshold].index
        thresh_data = self.frame[rows]
        out_path = self.out_path(f"Extracted Threshold {self.threshold}.xlsx")
        try:
            thresh_data.to_excel(out_path)
        except PermissionError as e:
            self.errors.append("Unable to write threshold data, the file may be open")

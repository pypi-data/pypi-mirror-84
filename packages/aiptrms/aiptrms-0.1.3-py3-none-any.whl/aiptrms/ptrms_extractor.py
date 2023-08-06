import os
import pandas as pd
from pandas.errors import EmptyDataError


class Ptrms:
    def __init__(self, file, ref_start, ref_end, sample_start, sample_end, threshold):
        self.file = file
        self.ref_start = ref_start
        self.ref_end = ref_end
        self.sample_start = sample_start
        self.sample_end = sample_end
        self.frame = pd.DataFrame
        self.errors = []
        self.threshold = int(threshold)
        self.dif = pd.DataFrame
        self.out_path = lambda x: os.path.join(
            os.path.dirname(self.file.name), x
        )

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
            self.frame.loc[int(self.ref_start) - 1: int(self.ref_end)]
                .drop(columns=["Cycle"], errors="ignore")
                .describe()
        )
        sample_window_stats = (
            self.frame.loc[int(self.sample_start) - 1: int(self.sample_end)]
                .drop(columns=["Cycle"], errors="ignore")
                .describe()
        )

        self.dif = sample_window_stats.transpose().sub(ref_window_stats.transpose())
        out_path = self.out_path(f"extracted_window.xlsx")
        try:
            self.dif.to_excel(out_path)
        except PermissionError as e:
            self.errors.append('Unable to write window data, the file may be open')
        if self.threshold:
            self.threshold_extract()

    def threshold_extract(self):
        rows = self.dif[self.dif['max'] > self.threshold].index
        thresh_data = self.frame[rows]
        out_path = self.out_path(f'Extracted Threshold {self.threshold}.xlsx')
        try:
            thresh_data.to_excel(out_path)
        except PermissionError as e:
            self.errors.append('Unable to write threshold data, the file may be open')
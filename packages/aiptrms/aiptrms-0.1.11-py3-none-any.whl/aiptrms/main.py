from tkinter import *

from aihelper import Browse, EntryBar, OkButton, Popup

from aiptrms import Ptrms


class UI:
    def __init__(self):
        self.data = None
        self.headers = None
        self.root = Tk()
        self.files = None
        self.button = None
        self.entrybar = EntryBar

    def looper(self):
        self.files = Browse(self.root, type="file", title="Select your file")
        self.entrybar = EntryBar(
            self.root,
            picks=[
                "Reference Cycle Start",
                "Reference Cycle End",
                "Sample Cycle Start",
                "Sample Cycle End",
                "Max Threshold",
            ],
        )

        self.button = OkButton(parent=self.root, function=self.load_data)
        self.root.mainloop()

    def load_data(self):
        try:
            ref_start = list(self.entrybar.get("Reference Cycle Start"))[0]
            ref_end = list(self.entrybar.get("Reference Cycle End"))[0]
            sample_start = list(self.entrybar.get("Sample Cycle Start"))[0]
            sample_end = list(self.entrybar.get("Sample Cycle End"))[0]
            try:
                threshold = list(self.entrybar.get("Max Threshold"))[0]
            except IndexError:
                threshold = None
            ptrms = Ptrms(
                self.files.get()[0],
                ref_start=ref_start,
                ref_end=ref_end,
                sample_start=sample_start,
                sample_end=sample_end,
                threshold=threshold,
            )
            ptrms.run()
            for error in ptrms.errors:
                Popup(self.root, error)

        except IndexError:
            Popup(self.root, "Please include all cycles required")


if __name__ == "__main__":
    UI().looper()

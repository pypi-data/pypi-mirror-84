import os
from tkinter import *

import seaborn as sns
from pandas import read_csv

from aiae.netzsch import Netzsch
from aihelper import Browse, EntryBar, OkButton, Popup

sns.set_theme()
sns.set()


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
            self.root, picks=["Ion", ("Alpha Min", 0.2), ("Alpha Max", 0.8)]
        )
        self.button = OkButton(parent=self.root, function=self.load_data)
        self.root.mainloop()

    def load_data(self):
        ion = list(self.entrybar.get("Ion"))
        if alpha_min := list(self.entrybar.get(("Alpha Min", 0.2))):
            alpha_min = [float(x) for x in alpha_min][0]
        if alpha_max := list(self.entrybar.get(("Alpha Max", 0.8))):
            alpha_max = [float(x) for x in alpha_max][0]

        self.data = Netzsch(
            self.files.get(), ion, alpha_max=alpha_max, alpha_min=alpha_min
        )
        self.data.run()


if __name__ == "__main__":
    UI().looper()

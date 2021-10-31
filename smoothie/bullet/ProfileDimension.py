from typing import List
from dataclasses import dataclass

import numpy.typing as npt
import numpy as np


@dataclass
class ProfileDimension:

    n_bins = 50

    name: str
    values: List
    weights: List
    binned_values: npt.ArrayLike = None
    bin_edges: npt.ArrayLike = None

    def normalize(self):
        self.binned_values = self.binned_values / np.sum(self.binned_values)


        
from typing import List
from dataclasses import dataclass

import numpy.typing as npt
import numpy as np


@dataclass
class ProfileDimension:

    n_bins = 50

    name: str
    song_ids: List
    values: List
    weights: List
    binned_values: npt.ArrayLike = None
    bin_edges: npt.ArrayLike = None
    song_buckets: List = None
    bin_width: float = None


    def normalize(self) -> None:
        self.binned_values = self.binned_values / np.sum(self.binned_values)

    
    def bin_values(
        self, 
        min_val: float, 
        max_val: float
    ) -> None:
        self.weights = self.weights / np.sum(self.weights)
        self.binned_values, self.bin_edges = np.histogram(
            self.values, 
            bins=ProfileDimension.n_bins,
            weights=self.weights,
            range=(min_val, max_val)
        )
        self.binned_values = self.binned_values.astype(np.float32)
        self.bin_edges[-1] += 0.1 # last right edge is inclusive; this helps with calculating bin indexes
        self.bin_width = (self.bin_edges[-1] - self.bin_edges[0]) / ProfileDimension.n_bins

        
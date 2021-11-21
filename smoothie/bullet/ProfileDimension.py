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
    _bin_width: float = None


    def normalize(self):
        self.binned_values = self.binned_values / np.sum(self.binned_values)

    
    def bin_values(self, min_val, max_val):
        self.binned_values, self.bin_edges = np.histogram(
            self.values, 
            bins=ProfileDimension.n_bins,
            weights=self.weights,
            range=(min_val, max_val)
        )
        self.binned_values = self.binned_values.astype(np.float32)
        self._bin_width = (self.binned_edges[-1] - self.bin_edges[0]) / ProfileDimension.n_bins
        self.hash_songs()

    
    def hash_songs(self):
        self._hashed_songs = [[] for _ in range(ProfileDimension.n_bins)]
        for i, song_id in enumerate(self.song_ids):
            bin = self.find_bin(self.values[i])
            self.song_buckets[bin].append(song_id)


    def find_bin(self, value):
        return int((value - self.bin_edges[0]) / self._bin_width)


        
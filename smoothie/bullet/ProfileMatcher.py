from typing import List

import numpy as np
import numpy.typing as npt
from scipy.ndimage.filters import gaussian_filter

from .ProfileDimension import ProfileDimension
from .SimilarityProfile import SimilarityProfile
from .SongProfile import SongProfile


class ProfileMatcher:

    blur_radius = 3

    def __init__(self):
        self.profiles = []
        self.similarity_profile = None


    # def get_similarity_profile(self):
    #     return self._similarity_profile


    def add_profile(self, profile):
        if len(self._profiles) >= 2:
            raise NotImplementedError('Matching is currently only supported for two profiles at a time!')

        self._profiles.append(profile)


    def add_profiles(self, profile_list):
        # TODO: figure out how to match more than two profiles, then implement
        pass
        

    def match_profiles(self):
        signed_similarity = {}
        for feature in SongProfile.relevant_features:
            dimensions = [profile.features[feature] for profile in self._profiles]
            self.bin_and_smooth_dimensions(dimensions)
            self.normalize_dimensions(dimensions)
            signed_similarity[feature] = self.calculate_signed_similarity(dimensions)
            continue

        self.similarity_profile = SimilarityProfile(signed_similarity)
        
        return self.similarity_profile



    def bin_and_smooth_dimensions(self, dimensions):
        min_val = min([min(dimension.values) for dimension in dimensions])
        max_val = max([max(dimension.values) for dimension in dimensions])
        for dimension in dimensions:
            dimension.bin_values(min_val, max_val)
            
            # use a Gaussian filter to smooth out details into overall features
            dimension.binned_values = gaussian_filter(dimension.binned_values, sigma=ProfileMatcher.blur_radius)


    def normalize_dimensions(self, dimensions):
        for dimension in dimensions:
            dimension.normalize()

    
    def calculate_signed_similarity(self, dimensions):
        # TODO: np.multiply() only takes two arguments. Be aware when matching more than 2 profiles
        return np.multiply(*[dimension.binned_values for dimension in dimensions])


    def create_playlist(self):
        """
            1. feature selection distribution
            2. decide what ranges to sample from
            3. if a profile doesn't have enough songs in the ranges, widen them
            4. sample equal numbers of songs from each profile

            1. selection distributions for all features
            2. loop over all songs
            3. for each song, generate a sample feature coordinate?
            4. sample song from that coordinate bin?
            issue: may not have song with that exact feature combination
        """
        for feature in SongProfile.relevant_features:
            pdf = self.similarity_profile.feature_selection_distribution(feature)
            samples = self.generate_samples(pdf)

            
        pass


    def generate_samples(
        self,
        selection_distribution: npt.ArrayLike
    ):
        while True:
            yield np.random.choice(len(selection_distribution), p=selection_distribution)


    @staticmethod
    def intervaled_integral(similarity, bin_edges):
        # use trapezoid rule
        return 0.5 * (similarity[:-1] + similarity[1:]) * np.diff(bin_edges)


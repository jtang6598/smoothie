from typing import List
from .ProfileDimension import ProfileDimension
from .SongProfile import SongProfile
import numpy as np
from scipy.ndimage.filters import gaussian_filter

class ProfileMatcher:

    blur_radius = 3

    def __init__(self):
        self._profiles = []


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
        # first bin profile data based on ranges for each dimension
        signed_similarity, similarity_profile = {}, {}
        bin_edges = None
        for feature in SongProfile.relevant_features:
            dimensions = [profile.features[feature] for profile in self._profiles]
            self.bin_and_smooth_dimensions(dimensions)
            self.normalize_dimensions(dimensions)
            signed_similarity[feature] = self.calculate_signed_similarity(dimensions)
            continue

            similarity_profile = ProfileMatcher.intervaled_integral(
                signed_similarity[feature], 
                dimensions[0].bin_edges
            )
        
        return signed_similarity



    def bin_and_smooth_dimensions(self, dimensions):
        min_val = min([min(dimension.values) for dimension in dimensions])
        max_val = max([max(dimension.values) for dimension in dimensions])
        for dimension in dimensions:
            dimension.binned_values, dimension.bin_edges = np.histogram(
                dimension.values, 
                bins=ProfileDimension.n_bins,
                weights=dimension.weights,
                range=(min_val, max_val)
            )
            dimension.binned_values = dimension.binned_values.astype(np.float32)
            # use a Gaussian filter to smooth out details into overall features
            dimension.binned_values = gaussian_filter(dimension.binned_values, sigma=ProfileMatcher.blur_radius)


    def normalize_dimensions(self, dimensions):
        for dimension in dimensions:
            dimension.normalize()

    
    def calculate_signed_similarity(self, dimensions):
        # TODO: np.multiply() only takes two arguments. Be aware when matching more than 2 profiles
        return np.multiply(*[dimension.binned_values for dimension in dimensions])


    @staticmethod
    def intervaled_integral(similarity, bin_edges):
        # use trapezoid rule
        return 0.5 * (similarity[:-1] + similarity[1:]) * np.diff(bin_edges)


from typing import List, Set

import numpy as np
import numpy.typing as npt

from util.bullet.ProfileDimension import ProfileDimension
from util.bullet.SimilarityProfile import SimilarityProfile
from util.bullet.SongProfile import SongProfile
from util import utils

from pandas import DataFrame, Series
from functools import reduce

class ProfileMatcher:

    blur_radius = 3
    songs_per_person = 10

    def __init__(self) -> None:
        self.profiles:  List[SongProfile] = []
        self.similarity_profile:  SimilarityProfile = None


    # def get_similarity_profile(self):
    #     return self._similarity_profile


    def add_profile(
        self, 
        profile: SongProfile
    ) -> None:
        self.profiles.append(profile)


    def add_profiles(
        self, 
        profile_list: List[SongProfile]
    ) -> None:
        self.profiles = self.profiles +  profile_list
        

    def match_profiles(self) -> SimilarityProfile:
        signed_similarity = {}
        for feature in SongProfile.relevant_features:
            dimensions = [profile.features[feature] for profile in self.profiles]
            self.bin_and_smooth_dimensions(dimensions)
            self._normalize_dimensions(dimensions)
            signed_similarity[feature] = self._calculate_signed_similarity(dimensions)
            continue

        self.similarity_profile = SimilarityProfile(signed_similarity)
        
        return self.similarity_profile


    def create_playlist(self) -> Set[str]:

        """
            1. get original selection distribution for all features
            2. loop over profiles. for each profile:
            3. assign some weight/probability to each song based on total probability across all features
            4. normalize song probabilities
            5. sample songs based on probabilities (make sure not to include duplicates)
        """
        original_selection_distribution = { 
            feature: self.similarity_profile.feature_selection_distribution(feature) 
                for feature in SongProfile.relevant_features
        }

        playlist_song_uris = set()
            
        for profile in self.profiles:
            # Calculate probabilities for each song and append column to df
            profile.df = profile.df.assign(selection_weight = lambda x: self._song_selection_weight(x, original_selection_distribution, profile))
            songs_to_add = profile.df.sample(
                n=10,
                axis=0,
                weights=profile.df.selection_weight
            ).uri
            for song_uri in songs_to_add:
                playlist_song_uris.add(song_uri)
            
            continue

        return playlist_song_uris


    def bin_and_smooth_dimensions(
        self, 
        dimensions: List[ProfileDimension]
    ) -> None:
        min_val = min([min(dimension.values) for dimension in dimensions])
        max_val = max([max(dimension.values) for dimension in dimensions])
        for dimension in dimensions:
            dimension.bin_values(min_val, max_val)
            
            # use a Gaussian filter to smooth out details into overall features
            dimension.binned_values = utils.gaussian_blur_1d(dimension.binned_values, ProfileMatcher.blur_radius)


    def _normalize_dimensions(
        self, 
        dimensions: List[ProfileDimension]
    ) -> None:
        for dimension in dimensions:
            dimension.normalize()

    
    def _calculate_signed_similarity(
        self, 
        dimensions: List[ProfileDimension]
    ) -> npt.ArrayLike:
        # TODO: np.multiply() only takes two arguments. Be aware when matching more than 2 profiles
        return reduce(lambda x, y: np.multiply(x, y), [dimension.binned_values for dimension in dimensions])
        


    def _song_selection_weight(
        self, 
        df: DataFrame, 
        selection_distribution: npt.ArrayLike, 
        profile: SongProfile
    ) -> Series:
        # TODO: how to make sure all feature weights are added?
        weights = {}
        for feature in SongProfile.relevant_features:
            profile_dimension = profile.features[feature]
            bins = (df[feature] - profile_dimension.bin_edges[0]) / profile_dimension.bin_width
            bins = bins.astype(int)
            weights[feature] = bins.apply(lambda x: selection_distribution[feature][x])

        weight = reduce(lambda x, y: x.add(y, fill_value=0), weights.values())
        weight = weight ** 2 / weight.sum()
        return weight


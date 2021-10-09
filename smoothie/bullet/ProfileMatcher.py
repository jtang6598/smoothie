from SongProfile import SongProfile
import numpy as np
from scipy.ndimage.filters import gaussian_filter

class ProfileMatcher:

    blur_radius = 5

    def __init__(self, similarity_profile):
        self._similarity_profile = similarity_profile


    def get_similarity_profile(self):
        return self._similarity_profile
        

    @classmethod
    def match(self, profile1: SongProfile, profile2: SongProfile):
        # first use a Gaussian filter to smooth out details into overall features
        profile1 = gaussian_filter(profile1.profile, sigma=ProfileMatcher.blur_radius)
        profile2 = gaussian_filter(profile2.profile, sigma=ProfileMatcher.blur_radius)

        signed_similarity = profile1 * profile2

        similarty_profile = ProfileMatcher.intervaled_integral(signed_similarity)
        return ProfileMatcher(similarty_profile)


    @classmethod
    def intervaled_integral(function):
        # use trapezoid rule
        return 0.5 * (function[:-1] + function[1:])



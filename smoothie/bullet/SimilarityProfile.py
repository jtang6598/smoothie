from typing import Dict

import numpy as np
import numpy.typing as npt

from .ProfileDimension import ProfileDimension


class SimilarityProfile:

    def __init__(
        self,
        feature_similarities: Dict[str, npt.ArrayLike]
    ) -> None:
        self.feature_similarities = feature_similarities


    def feature_profile(self, feature):
        return self.feature_similarities[feature]


    def feature_selection_distribution(
        self, 
        feature: str,
        area_fraction: float = 0.5,
        tol: float = 0.01
    ):
        """
        The specified feature of the similarity profile is square to amplify 
        regions of high similarity. The squared feature is then normalized to 
        create a probability distribution function.
        """
        squared_similarity = self.feature_similarities[feature] ** 2
        cutoff_y = self.fractional_area_y_value(squared_similarity, area_fraction, tol)
        for i, similarity in  enumerate(squared_similarity):
            squared_similarity[i] = max(0, similarity - cutoff_y)

        return squared_similarity / np.sum(squared_similarity)


    def fractional_area_y_value(
        self,
        similarity: npt.ArrayLike, 
        fraction: float, 
        tol: float
    ):
        total_area = np.sum(similarity)
        y = total_area * fraction / ProfileDimension.n_bins
        lower_area = self.find_lower_area(similarity, y)
        proportion = lower_area / total_area
        while abs(proportion - fraction) > tol:
            y *= fraction / proportion
            lower_area = self.find_lower_area(similarity, y)
            proportion = lower_area / total_area

        return y
            


    def find_lower_area(
        self,
        similarity: npt.ArrayLike,
        y: float
    ):
        area = 0
        for bin in similarity:
            area += min(bin, y)
        return area


        
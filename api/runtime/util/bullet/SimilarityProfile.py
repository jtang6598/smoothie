from typing import Dict

import numpy as np
import numpy.typing as npt

from api.runtime.util.bullet.ProfileDimension import ProfileDimension
from api.runtime.util import utils


class SimilarityProfile:

    def __init__(
        self,
        feature_similarities: Dict[str, npt.ArrayLike]
    ) -> None:
        self.feature_similarities = feature_similarities


    def feature_profile(
        self, 
        feature: str
    ) -> npt.ArrayLike:
        return self.feature_similarities[feature]


    def feature_selection_distribution(
        self, 
        feature: str,
        area_fraction: float = 0.5,
        tol: float = 0.01
    ) -> npt.ArrayLike:
        """
        The specified feature of the similarity profile is square to amplify 
        regions of high similarity. The squared feature is then normalized to 
        create a probability distribution function.
        """
        squared_similarity = self.feature_similarities[feature] ** 2
        cutoff_y = self._fractional_area_y_value(squared_similarity, area_fraction, tol)
        for i, similarity in  enumerate(squared_similarity):
            squared_similarity[i] = max(0, similarity - cutoff_y)

        return utils.normalize_array(squared_similarity)


    def _fractional_area_y_value(
        self,
        similarity: npt.ArrayLike, 
        fraction: float, 
        tol: float
    ) -> float:
        total_area = np.sum(similarity)
        y = total_area * fraction / ProfileDimension.n_bins
        lower_area = self._find_lower_area(similarity, y)
        proportion = lower_area / total_area

        # find y value that splits the curve's area in half
        while abs(proportion - fraction) > tol:
            y *= fraction / proportion
            lower_area = self._find_lower_area(similarity, y)
            proportion = lower_area / total_area

        return y
            


    def _find_lower_area(
        self,
        similarity: npt.ArrayLike,
        y: float
    ) -> float:
        area = 0
        for bin in similarity:
            area += min(bin, y)
        return area


        
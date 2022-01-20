

from pandas import DataFrame
from api.runtime.util.data_objects.User import User
from api.runtime.util.bullet.ProfileDimension import ProfileDimension


class SongProfile:

    relevant_features = [
        'acousticness',
        'danceability',
        'energy', 
        'instrumentalness',
        'loudness',
        'mode', 
        'speechiness',
        'tempo', 
        'time_signature',
        'valence',
    ]

    def __init__(
        self, 
        user: User, 
        song_df: DataFrame
    ) -> None:
        self.features = { feature: ProfileDimension for feature in SongProfile.relevant_features }
        self.df = song_df[[*SongProfile.relevant_features, 'uri']]
        self.user = user
        for feature in self.features:
            dimension_songids = list(song_df.id)
            dimension_values = list(song_df[feature])
            dimension_weights = list(song_df.weight)
            self.features[feature] = ProfileDimension(feature, dimension_songids, dimension_values, dimension_weights)

    
    def feature_profile(
        self, 
        feature: str
    ) -> ProfileDimension:
        return self.features[feature]

        
        


    



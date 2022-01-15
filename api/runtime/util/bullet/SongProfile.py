

from .ProfileDimension import ProfileDimension


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

    def __init__(self, user, song_df):
        self.features = { feature: None for feature in SongProfile.relevant_features }
        for feature in self.features:
            dimension_songids = list(song_df.id)
            dimension_values = list(song_df[feature])
            dimension_weights = list(song_df.weight)
            self.features[feature] = ProfileDimension(feature, dimension_songids, dimension_values, dimension_weights)

    
    def feature_profile(self, feature):
        return self.features[feature]

        
        


    



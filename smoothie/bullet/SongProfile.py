

from smoothie.data_objects.Playlist import Playlist


class SongProfile:

    step_size = 0.01
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

    def __init__(self, user, playlists): # our playlist type should have a list of all our songs 
        return
        self._profile = { feature: 0 for feature in SongProfile.relevant_features }
        for playlist in  playlists:
            # should be able to replace these nested for loops with a single for loop if using pandas.
            # just add the column sum for each feature.
            for song in playlist:
                for feature in  relevant_features:
                    self._profile[feature] += song[feature]
        


    



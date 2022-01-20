from runtime.util.bullet.ProfileMatcher import ProfileMatcher
from runtime.util.bullet.SongProfile import SongProfile
import pandas as pd


def test_create_playlist():
    wanted_playlists = ['BOPIS (poop 3.2.2)', 'semi-chill (aka poop 2.7)']
    song_dfs = []
    for i, name in enumerate(wanted_playlists):
        song_dfs.append(pd.read_csv(name + '.csv', index_col=0))

    matcher = ProfileMatcher()
    for song_df in song_dfs:
        matcher.add_profile(SongProfile(None, song_df))

    similarity_profile = matcher.match_profiles()
    similarity = similarity_profile.feature_similarities
    matcher.create_playlist()

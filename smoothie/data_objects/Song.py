from dataclasses import dataclass

@dataclass
class Song:
    '''
    Based on Spotify's AudioFeaturesObject
    '''
    acousticness: float
    analysis_url: str
    danceability: float
    duration_ms: int
    energy: float
    id: str
    instrumentalness: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    track_href: str
    type: str
    uri: str
    valence: float

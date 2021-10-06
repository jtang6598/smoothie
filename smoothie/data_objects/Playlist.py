from typing import Type
from Song import Song

class Playlist:

    def __init__(self):
        self._songs = []


    def add_songs(self, songs):
        try:
            self._songs += songs
        except TypeError:
            self._songs.append(songs)

    
    def __iter__(self):
        return iter(self._songs)
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter


class SpotifyUser():
    access_token: str

    def __init__(self) -> None:
        scope = 'user-read-recently-played user-top-read user-library-read'
        self.auth_manager = SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                         client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                         redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
                                         scope=scope)
        self.sp = spotipy.Spotify()
        self.top_genres = None
        self.top_genres_artists = None

    def generate_access_token_and_login(self, code):
        self.access_token = self.auth_manager.get_access_token(code)["access_token"]
        self.sp = spotipy.Spotify(auth=self.access_token)

    def get_oauth_url(self):
        return self.auth_manager.get_authorize_url()

    def get_top_genres(self, term):
        results = self.sp.current_user_top_artists(time_range=term, limit=100)
        all_genres = [genre for r in results['items'] for genre in r['genres']]
        top_genres = Counter(all_genres)
        self.top_genres = {key: value for key, value in sorted(
            top_genres.items(), key=lambda k: k[1], reverse=True)}
        self.top_genres_artists = [[r['name'], r['id'], r['genres']] if len(
            r['genres']) > 0 else [r['name'], r['id'], ['unknown genre']] for r in results['items']]

    def select_genre(self, idx=0):
        return list(self.top_genres.keys())[idx]

    def get_genre_artists(self, genre):
        artists = []
        for name, _, genres in self.top_genres_artists:
            if genre in genres:
                artists.append(name)
        artists = ", ".join(artists)
        return artists

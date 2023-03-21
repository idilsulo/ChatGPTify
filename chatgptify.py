import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from chatgpt_wrapper import ChatGPT
import textwrap


class SpotifyTrack():
    def __init__(self, uri, name, artist, album):
        self.uri = uri
        self.name = name
        self.artist = artist
        self.album = album


class SpotifyPlaylist():
    def __init__(self) -> None:
        
        scope = scope = 'playlist-modify-public playlist-modify-private user-library-read'
        
        self.bot =  ChatGPT()
        self.sp  = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
                                               scope=scope))

        self.playlist = None
        self.name = "Chat-GPT presents..."

        self.playlist_response = None
        self.last_response = None
    

    def ask_chatgpt(self, prompt : str, prompt_type : str = "", display=True):
        print("Asking ChatGPT...")
        
        if prompt_type == "playlist": 
            prompt = "Provide a playlist containing songs " + prompt
        elif prompt_type == "name":
            prompt = "What might be a suitable and creative name for this playlist?" \
                     " Only provide the name and no other details."
       
        success, response, message = self.bot.ask(prompt)

        if not success:
            raise RuntimeError(message)

        if prompt_type == "playlist": self.playlist_response = response
        if prompt_type == "name": self.name = response.replace('"','')
        self.last_response = response
        
        if display:
            width = 70
            print("-" * width)
            print("     " * (width // 11) + "Chat-GPT")
            prompt_str = textwrap.fill("Prompt: " + prompt)
            print(prompt_str)
            print("-" * width)
            display_str = textwrap.fill(response)
            print(display_str)
            print()
            print("-" * width)
    

    def create_playlist(self):
        query = self.playlist_response.split('\n\n')[2].split('\n')
        query = [q[q.find('. ')+2:].replace('"', '') for q in query]

        print("Creating playlist...")
        playlist = []
        for q in query:
            try:
                r = self.sp.search(q)
                item = r['tracks']['items'][0]  # Select the first track
                track = SpotifyTrack(uri=item['uri'], name=item['name'], artist=item['artists'], album=item['album'])
                playlist.append(track)
            except:
                print("Track not found: ", q)

        self.playlist = playlist

    
    def save_playlist(self, name : str = ""):
        print("Saving to library...")

        if not name: name = self.name

        user_id = self.sp.current_user()['id']
        self.sp.user_playlist_create(user=user_id, name=name, public=True)

        p_id = None
        for playlist in self.sp.user_playlists(user_id)['items']:
            if playlist['name'] == name:
                p_id = playlist['id']
                break
        
        tracks = [track.uri for track in self.playlist]
        self.sp.user_playlist_add_tracks(user=user_id, playlist_id=p_id, tracks=tracks)


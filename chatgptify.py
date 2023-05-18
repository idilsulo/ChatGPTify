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
        scope = 'playlist-modify-public playlist-modify-private user-library-read'
        
        self.bot =  ChatGPT()
        self.sp  = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
                                               scope=scope))

        self.playlist = None
        self.name = "ChatGPT presents..."

        self.playlist_response = None
        self.last_response = None
    

    def ask_chatgpt(self, prompt : str, prompt_type : str = "", display=True) -> None:
        """Ask prompt to ChatGPT

        Args:
            prompt (str): User prompt to ask. 
                * prompt_type = "playlist" - A fixed start string is appended: 
                    "Provide a playlist containing songs " ...
                * prompt_type = "name" - Prompt is fixed, provided string is not considered
                    "What might be a suitable and creative name for this playlist?" \
                     " Only provide the name and no other details."
                * prompt_type = "" - User can ask any prompt
            
            prompt_type (str, optional): Selects the type of prompt. Defaults to "".
                * prompt_type = "playlist" - For playlist song suggestion
                * prompt_type = "name"     - For playlist name suggestion
                * prompt_type = ""         - Unrestricted prompts 

            display (bool, optional): Whether to display ChatGPT output. Defaults to True.

        Raises:
            RuntimeError: Upon ChatGPT execution failure.
        """        
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
        if prompt_type == "name": self.name = str(response.replace('"',''))
        self.last_response = response
        
        if display:
            width = 70
            print("-" * width)
            print("     " * (width // 11) + "ChatGPT")
            prompt_str = textwrap.fill("Prompt: " + prompt)
            print(prompt_str)
            print("-" * width)
            display_str = textwrap.fill(response)
            print(display_str)
            print()
            print("-" * width)
    

    def create_playlist(self) -> None:
        """Queries Spotify API to retrieve tracks 
        """        
        query = self.playlist_response[self.playlist_response.find('1.'):].split('\n\n')[0].split('\n')
        query = [q[q.find('. ')+2:].replace('"', '') for q in query]

        print("Creating playlist...")
        playlist = []
        for q in query:
            try:
                if 'by' in q:
                    name, artist = q.split(' by ')
                    if '-' in artist: artist = artist[:artist.find('-')]
                    search_q = "{}%10artist:{}".format(name, artist)
                    r = self.sp.search(search_q)
                elif '-' in q:
                    name, artist = q.split(' - ')
                    search_q = "{}%10artist:{}".format(name, artist)
                    r = self.sp.search(search_q)
                else:
                    r = self.sp.search(q)
                item = r['tracks']['items'][0]  # Select the first track
                track = SpotifyTrack(uri=item['uri'], name=item['name'], 
                                     artist=item['artists'], album=item['album'])
                playlist.append(track)
            except:
                print("Track not found: {}".format(q))

        self.playlist = playlist

    
    def save_playlist(self, name : str = "") -> None:
        """Saves the created playlist under user account

        Args:
            name (str, optional): Name of the playlist. Uses the name created by ChatGPT or
                default name when not specified
        """
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


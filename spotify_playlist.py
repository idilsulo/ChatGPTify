
from utils import *

# os.environ['SPOTIFY_CLIENT_ID']     = "Spotify Client ID"
# os.environ['SPOTIFY_CLIENT_SECRET'] = "Spotify Client Secret"
# os.environ['SPOTIFY_REDIRECT_URI']  = "Redirect URI, can be localhost e.g. http://localhost:8080"


if __name__ == "__main__":

    play = SpotifyPlaylist()

    # Ask for a playlist to Chat-GPT similar to a style of an artist, a genre and so on
    # Provide: prompt_type = playlist
    # Examples:
    #   - similar to the style of Quantic and Thievery Corporation without including these artists
    #   - falling under the genre downtempo and trip-hop
    play.ask_chatgpt(prompt="similar to the ones created by Daniel Avery",
                     prompt_type="playlist")
    play.create_playlist()

    # Ask for a playlist name, you can also save the playlist without asking 
    # Povide: prompt_type = name
    play.ask_chatgpt(prompt="", prompt_type="name")
    play.save_playlist(name=play.name)

    # Ask for the common elements in these songs for reasoning
    play.ask_chatgpt(prompt="What is the common theme, musical elements or features in this playlist? Explain in detail.")
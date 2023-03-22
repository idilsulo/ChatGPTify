import argparse
import distutils.util
from chatgptify import *
from user import User
import textwrap

# os.environ['SPOTIFY_CLIENT_ID']     = "Spotify Client ID"
# os.environ['SPOTIFY_CLIENT_SECRET'] = "Spotify Client Secret"
# os.environ['SPOTIFY_REDIRECT_URI']  = "Redirect URI, can be localhost e.g. http://localhost:8080"


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--USER_DATA", type=lambda x: bool(distutils.util.strtobool(x)), required=False, 
                        default=False, 
                        help="Whether to provide listening history to ChatGPT for playlist suggestion.")

    parser.add_argument("--TERM", type=str, required=False, 
                        default="long_term", 
                        help="For suggestions considering artists listened in "\
                             "long_term (for years), " \
                             "medium_term (for past 6 months), " \
                             "short_term (for past 4 weeks)")
    
    parser.add_argument("--TOP_GENRE", type=int, required=False, 
                        default=1, 
                        help="Top # genre that is: "\
                             "1 (most listened), " \
                             "2 (second most listened), " \
                             "3 (third most listened)")
    
    parser.add_argument("--PROMPT", type=str, required=False, 
                        default="similar to the ones created by Daniel Avery", 
                        help="Write a prompt that completes the following sentence: \n"\
                             "Provide a playlist containing songs...")

    parser.add_argument("--PLAYLIST_NAME", type=str, required=False, 
                        default="", 
                        help="If specified with a custom string, this is used as the playlist name. \n" \
                             "Otherwise, name suggestion from ChatGPT is used.")

    args = parser.parse_args()

    play = SpotifyPlaylist()

    if args.USER_DATA:
        u = User(term=args.TERM)
        u.get_top_genres()                                    # Request user top artists & their genres
        selected_genre = u.select_genre(idx=args.TOP_GENRE-1) # Most listened genre
        artists = u.get_genre_artists(genre=selected_genre)   # Get user artists in this genre

        width = 70
        print("-" * width)
        print("Top #{} Listened Genre: {}".format(args.TOP_GENRE, selected_genre))
        print(textwrap.fill("Artists              : {}".format(artists)))
        print("-" * width)

        play.ask_chatgpt(prompt="Suggest new artists in the same genre with " + artists,
                         prompt_type="")
        play.ask_chatgpt(prompt="Create a playlist featuring the new artists. Provide first the song name followed by the artist.",
                         prompt_type="playlist")
    else:
        # Ask for a playlist to ChatGPT 
        # Provide: prompt_type = playlist
        # Examples:
        #   - similar to the style of Quantic and Thievery Corporation without including these artists
        #   - falling under the genre downtempo and trip-hop
        play.ask_chatgpt(prompt=args.PROMPT,
                         prompt_type="playlist")
    
    play.create_playlist()
    
    if not args.PLAYLIST_NAME: 
        # Ask ChatGPT for a playlist name
        # Provide: prompt_type = name
        play.ask_chatgpt(prompt="", prompt_type="name")
        play.save_playlist(name=play.name)
    else:
        play.save_playlist(name=args.PLAYLIST_NAME)

    # Ask for the common elements in these songs for reasoning
    play.ask_chatgpt(prompt="What is the common theme, musical elements or features in this playlist? Explain in detail.")
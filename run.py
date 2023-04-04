import argparse
import distutils.util
from chatgptify import SpotifyPlaylist
from user import SpotifyUser
import textwrap
from dotenv import load_dotenv
from chatgpt_wrapper import OpenAIAPI
load_dotenv()

# os.environ['SPOTIFY_CLIENT_ID']     = "Spotify Client ID"
# os.environ['SPOTIFY_CLIENT_SECRET'] = "Spotify Client Secret"
# os.environ['SPOTIFY_REDIRECT_URI']  = "Redirect URI, can be localhost e.g. http://localhost:8080"

def ask_chatgpt(bot, prompt):
    success, response, message = bot.ask(prompt)
    if not success:
        raise RuntimeError(message)
    return response

class GptifyArgsTerm:
    long_term = "long_term"
    medium_term = "medium_term"
    short_term = "short_term"


class GptifyArgs:
    USER_DATA: str
    TERM: GptifyArgsTerm
    TOP_GENRE: int
    PLAYLIST_NAME: str
    PROMPT: str

def run_prompting(args: GptifyArgs, user: SpotifyUser, play: SpotifyPlaylist, bot:OpenAIAPI):

    if args.USER_DATA:
        # Request user top artists & their genres
        user.get_top_genres(args.TERM)
        selected_genre = user.select_genre(
            idx=args.TOP_GENRE-1)  # Most listened genre
        # Get user artists in this genre
        artists = user.get_genre_artists(genre=selected_genre)

        width = 70
        print("-" * width)
        print("Top #{} Listened Genre: {}".format(
            args.TOP_GENRE, selected_genre))
        print(textwrap.fill("Artists              : {}".format(artists)))
        print("-" * width)

        ask_chatgpt(bot, prompt="Suggest new artists in the same genre with " + artists)
        ask_chatgpt(bot, "Create a playlist featuring the new artists. Provide first the song name followed by the artist.")
    else:
        # Ask for a playlist to ChatGPT
        # Examples:
        #   - similar to the style of Quantic and Thievery Corporation without including these artists
        #   - falling under the genre downtempo and trip-hop
        response = ask_chatgpt(bot, prompt="Provide a playlist containing songs" + args.PROMPT)
        play.save_playlist

    play.create_playlist()
    playlist_url = None
    if not args.PLAYLIST_NAME:
        # Ask ChatGPT for a playlist name
        # Provide: prompt_type = name
        playlist_name = ask_chatgpt(bot, prompt="What might be a suitable and creative name for this playlist?\n Only provide the name and no other details.")
        playlist_url = play.save_playlist(name=playlist_name)
    else:
        playlist_url = play.save_playlist(name=args.PLAYLIST_NAME)

    # Ask for the common elements in these songs for reasoning
    analysis = play.ask_chatgpt(
        prompt="What is the common theme, musical elements or features in this playlist? Explain in detail.")
    return [playlist_url, analysis, artists, ]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--USER_DATA", type=lambda x: bool(distutils.util.strtobool(x)), required=False,
                        default=False,
                        help="Whether to provide listening history to ChatGPT for playlist suggestion.")

    parser.add_argument("--TERM", type=str, required=False,
                        default="long_term",
                        help="For suggestions considering artists listened in "
                             "long_term (for years), "
                             "medium_term (for past 6 months), "
                             "short_term (for past 4 weeks)")

    parser.add_argument("--TOP_GENRE", type=int, required=False,
                        default=1,
                        help="Top # genre that is: "
                             "1 (most listened), "
                             "2 (second most listened), "
                             "3 (third most listened)")

    parser.add_argument("--PROMPT", type=str, required=False,
                        default="similar to the ones created by Daniel Avery",
                        help="Write a prompt that completes the following sentence: \n"
                             "Provide a playlist containing songs...")

    parser.add_argument("--PLAYLIST_NAME", type=str, required=False,
                        default="",
                        help="If specified with a custom string, this is used as the playlist name. \n"
                             "Otherwise, name suggestion from ChatGPT is used.")

    args = parser.parse_args()
    play = SpotifyPlaylist()
    user = SpotifyUser()
    bot = OpenAIAPI()
    run_prompting(args, user, play, bot)

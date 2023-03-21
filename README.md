# ChatGPTify = 🤖 ChatGPT x Spotify 🎧

Maybe you have already tried asking or song recommendations to ChatGPT, but wouldn't it be nice if you could listen the playlists recommended based on your music taste directly on your Spotify account?

This repository is built with Python and uses [spotipy](https://github.com/spotipy-dev/spotipy) and [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper) for creating playlists based on user prompts via [ChatGPT](https://openai.com/blog/chatgpt) model.


## Installation

**Step 1:** Create an [OpenAI account](https://beta.openai.com/account/api-keys)

**Step 2:** Generate [Spotify Client ID & Secret Key](https://developer.spotify.com/dashboard/login)

**Step 3:** Install dependencies

```
pip install spotipy
pip install git+https://github.com/mmabrouk/chatgpt-wrapper
playwright install firefox
chatgpt install
```

**Note:** The final command will then log in with your browser. If you encounter any issues regarding ChatGPT wrapper installation, please refer to [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper).


**Step 4:** Setup credentials
This can be done via executing the following commands on Terminal.
```
export SPOTIFY_CLIENT_ID="Spotify Client ID"
export SPOTIFY_CLIENT_SECRET"Spotify Client Secret"
export SPOTIFY_REDIRECT_URI= "Redirect URI, e.g. http://localhost:8080"
```

OR, can be modified inside the Python script, `spotify_playlist.py`:
```
os.environ['SPOTIFY_CLIENT_ID']     = "Spotify Client ID"
os.environ['SPOTIFY_CLIENT_SECRET'] = "Spotify Client Secret"
os.environ['SPOTIFY_REDIRECT_URI']  = "Redirect URI"
```

## Usage 

For a sample usage of the script, run
```
python3 spotify_playlist.py
```

## Examples

```
play = SpotifyPlaylist()
```

Ask for a playlist recommendation by setting `prompt_type="playlist"`.
Prompts will then automatically start with the phrase: `"Provide a playlist containing songs "`

You can complete the prompt as you wish, see examples:

* `"similar to the style of Quantic and Thievery Corporation without including these artists"`
* `"falling under the genre downtempo and trip-hop"`

```
play.ask_chatgpt(prompt="similar to the ones created by Daniel Avery", prompt_type="playlist")
```

You can then create and save the playlist:
```
play.create_playlist()
play.save_playlist()
```

Additionally you can ask for a playlist name and save the playlist under your account with this name, provide `prompt_type="name"`:

```
play.ask_chatgpt(prompt="", prompt_type="name")
play.save_playlist(name=play.name)
```

You can also ask the reasoning behind this playlist by asking the common elements in these songs, no `prompt_type` required:
```
play.ask_chatgpt(prompt="What is the common theme, musical elements or features in this playlist? Explain in detail.")
```

Enjoy your new playlists!
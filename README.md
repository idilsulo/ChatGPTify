# ChatGPTify = 🤖 ChatGPT x Spotify 🎧

Maybe you have already tried asking for song recommendations to ChatGPT, but wouldn't it be nice if you could listen the playlists recommended based on your music taste directly on your Spotify account?

<p align="center">
<img src=assets/playlist.jpg  width="500">
</p>

> **ChatGPT Playlist reasoning:** The playlist "Electronic Odyssey" consists of electronic dance music tracks that share several common themes, musical elements, and features. These tracks are characterized by their pulsing beats, hypnotic rhythms, and driving basslines that create an intense and immersive listening experience.  One common theme in this playlist is the use of repetition, which is a hallmark of electronic music. The tracks often feature looping melodies, hypnotic arpeggios, and other repetitive elements that create a sense of momentum and progression. This repetition is often used to build tension and energy, leading to cathartic drops and climactic moments.  Another common feature of these tracks is their use of synthesizers and other electronic instruments to create a wide range of sounds and textures. The tracks often feature lush pads, soaring leads, and intricate percussion that are layered and manipulated to create complex and evolving soundscapes. 


This repository is built with Python and uses [spotipy](https://github.com/spotipy-dev/spotipy) and [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper) for creating playlists based on user prompts via [ChatGPT](https://openai.com/blog/chatgpt) model.


## Installation

**Step 1:** Create an [OpenAI account](https://beta.openai.com/account/api-keys)

**Step 2:** Generate [Spotify Client ID & Secret Key](https://developer.spotify.com/dashboard/login) and set a Redirect URI under your App settings, e.g. `http://localhost:8080`.

**Step 3:** Install dependencies

```
pip install spotipy
pip install git+https://github.com/mmabrouk/chatgpt-wrapper@18f3903cc083a794ec1b4e55e82f0e7ac5184f35
playwright install firefox
chatgpt install
```

This will then open up a browser window. Log in to ChatGPT in the browser window, walk through all the intro screens and then exit.

```
1> /exit
```

**Note:**  If you encounter any issues regarding ChatGPT wrapper installation, please refer to [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper).


**Step 4:** Setup credentials

This can be done via executing the following commands on Terminal.
```
export SPOTIFY_CLIENT_ID="Spotify Client ID"
export SPOTIFY_CLIENT_SECRET="Spotify Client Secret"
export SPOTIFY_REDIRECT_URI="Redirect URI, e.g. http://localhost:8080"
```

OR, can be modified inside the Python script, `run.py`:
```
os.environ['SPOTIFY_CLIENT_ID']     = "Spotify Client ID"
os.environ['SPOTIFY_CLIENT_SECRET'] = "Spotify Client Secret"
os.environ['SPOTIFY_REDIRECT_URI']  = "Redirect URI"
```

**Important:** Make sure to set the same Redirect URI on your Spotify Developer account as well. This can be done under `Dashboard > App > Edit Settings > Redirect URIs`.

## Usage 

For a sample usage of the script, run
```
python3 run.py
```

### Prompting for Playlists

Custom user prompts can be provided in a way that they will complete the following sentence: 
`"Provide a playlist containing songs..."`
```
python3 run.py --PROMPT "falling under the genre downtempo and trip-hop" 
```

This will create the playlist and save it with a ChatGPT-generated name. If you instead would like to save it with a custom name, this can be provided with `--PLAYLIST_NAME` flag.

**Note:** Using this option will **NOT** use or share your previously listened artists with ChatGPT.

### Prompting for Playlists with User Data / Listening History

If you would like to share your previously listened artists and get playlists with new artist recommendations, simply use:
```
python3 run.py --USER_DATA True --TERM long_term --TOP_GENRE 1
```

This will create playlist that are similar to but (mostly) not including your top-listened artists in the past years. The time range (term) and top genre selection can be made in the following way:

```
--TERM      "long_term"    # past years
            "medium_term   # past 6 months
            "short_term    # past 4 weeks
    
--TOP_GENRE 1              # top (most-listened) genre
            2              # second most listened genre
            3              # third most listened genre
```

**Note:** If you would like to have better quality predictions, try executing `pkill firefox` and then `chatgpt install` once in a while.

## Examples

Feel free to plug and play!

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
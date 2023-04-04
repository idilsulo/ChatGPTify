import sqlite3
from dotenv import load_dotenv
from flask import Flask, render_template, request, g

from chatgptify import SpotifyPlaylist
from run import run_prompting, GptifyArgs
from user import SpotifyUser
from chatgpt_wrapper import OpenAIAPI
load_dotenv()

app = Flask(__name__)

play = SpotifyPlaylist()
user = SpotifyUser()
bot = OpenAIAPI()
connected_spotify_auth = False

# DB RELATED
DATABASE = 'file.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def fetch_table():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM my_table')
    rows = cur.fetchall()
    return str(rows)
# DB RELATED


@app.route('/')
def hello_world():
    return render_template('hello.html', name="stranger", spotify_url=user.get_oauth_url())


@app.route('/spotify_auth')
def spotify_auth():
    spotify_code = request.args.get("code", None)
    assert spotify_code, "Called without code, error?"
    user.generate_access_token_and_login(spotify_code)
    global connected_spotify_auth
    connected_spotify_auth = True
    user_info = user.sp.current_user()
    user_display_name = user_info['display_name']
    return render_template('hello.html', name=user_display_name, spotify_url=user.get_oauth_url())


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    playlist_name = request.form['playlist_name']
    term = request.form['term']
    top_genre = request.form.get('top_genre')
    prompt = request.form.get('prompt')
    args = GptifyArgs()

    args.TERM = term
    args.USER_DATA = connected_spotify_auth
    args.TOP_GENRE = top_genre
    args.PLAYLIST_NAME = playlist_name
    args.PROMPT = prompt
    [playlist_url, analysis] = run_prompting(args, user, play, bot)
    return render_template('hello.html', name="name", spotify_url=user.get_oauth_url(), playlist_url=playlist_url, analysis=analysis)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

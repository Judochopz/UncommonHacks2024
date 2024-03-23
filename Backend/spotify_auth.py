import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Get username from terminal
username = sys.argv[1]

# Load environment variables from .env file
load_dotenv()

# Import environment variables from .env
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")


# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

spotifyObject = spotipy.Spotify(auth=token)

# Redirected to https://www.google.com/?code=AQCE2TZ_-SHV99GM_VcVNeKl2Q0kBTlO-lU3LvUHq2ynfKD1FTVjt35hvlkMNbenx41usEyQO2ja_HL1koOZ3Q1QOz2OsDLf2s440nB7IG0wBjXNwKTcPHQJXAURbQHLkpAGBz9RGjatF89SAjhkslXwD8FBaw

user = spotifyObject.current_user()
print(json.dumps(user, sort_keys=True, indent=4))


sp = SpotifyOAuth (
        client_id = os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=url_for('authorize', _external=True),
        scope="user-library-read user-top-read"
    ) 
# # Get the user's saved tracks
# results = user.current_user_saved_tracks()

# # Iterate over saved tracks and print their names
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx + 1, track['artists'][0]['name'], "–", track['name'])
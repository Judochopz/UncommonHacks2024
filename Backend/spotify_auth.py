import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

def spotifyAuth(username):
    # Get username from terminal
    # username = sys.argv[1]

    # Load environment variables from .env file
    load_dotenv(".env")

    # Import environment variables from .env
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    print(client_id, client_secret, redirect_uri)
    # Save scope
    scope = "user-read-recently-played user-top-read "

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username)
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username)

    spotifyObject = spotipy.Spotify(auth=token)

    user = spotifyObject.current_user()
    # print(json.dumps(user, sort_keys=True, indent=4))

    # displayName = user['display_name']

    sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope
            )
        )
    return (sp, user)

# for i, item in enumerate(results['items']):
#         print(i, item['name'], '//', item['artists'][0]['name'])
#     print()
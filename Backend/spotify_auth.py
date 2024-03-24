import os
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

def spotifyAuth(username):
    # Load environment variables from .env file
    load_dotenv(".env")

    # Import environment variables from .env
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    # Save scope
    scope = "user-read-recently-played user-top-read user-read-private"

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username)
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username)

    spotifyObject = spotipy.Spotify(auth=token)

    user = spotifyObject.current_user()
    
    # Create spotipy object for API calls
    sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope
            )
        )
    return (sp, user)
"""
This tool is used to get a refresh token for a given access token.
The output of this tool is a refresh token that have to be set in the .env file
"""

import os

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(override=True)

SPOTIPY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIFY_URI")

auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,  # Same as the one in your app
    scope="playlist-read-private",  # Scope to read private playlists
)

access_token = auth_manager.get_access_token()
print(access_token["refresh_token"])

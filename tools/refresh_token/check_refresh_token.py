"""
This script checks if the refresh token is valid.
Before running this script, you need to set the refresh token in the .env file.
"""

import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(override=True)

SPOTIPY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIFY_URI")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,  # Same as the one in your app
    scope="playlist-read-private",  # Scope to read private playlists
)

auth_manager.refresh_access_token(REFRESH_TOKEN)
sp = spotipy.Spotify(auth_manager=auth_manager)

print(sp.current_user())

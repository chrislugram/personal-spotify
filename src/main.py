import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# TODO include env variables
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

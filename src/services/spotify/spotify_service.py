"""
This class is responsible for consuming the Spotify API
"""

from dataclasses import dataclass
from typing import Any, List

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


@dataclass
class SpotifyService:
    """
    This class is responsible for consuming the Spotify API
    """

    def __init__(self, client_id: str, client_secret: str, uri: str):
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=uri,
                scope="playlist-read-private",
            )
        )

    def _safe_call(self, func, *args, **kwargs) -> Any:
        """
        This method is used to call a function safely

        Args:
            func (function): The function to call
            args (tuple): The arguments to pass to the function
            kwargs (dict): The keyword arguments to pass to the function

        Returns:
            Any: The return value of the function
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error calling {func.__name__}: {e}")

    def get_user(self) -> dict:
        """
        This method is used to get the user

        Returns:
            Any: The return value of the function
        """
        return self._safe_call(self.sp.current_user)

    def get_playlists(self, limit: int = 50) -> List:
        """
        This method is used to get the user's playlists

        Args:
            limit (int): The maximum number of items to return

        Returns:
            Any: The return value of the function
        """
        playlists = []
        offset = 0
        while True:
            response = self._safe_call(
                self.sp.current_user_playlists, limit=limit, offset=offset
            )

            # Check if the response is valid
            if not response or "items" not in response:
                break

            # Add the items to the list
            playlists.extend(response["items"])

            # Check if there are more items
            if response["next"] is None:
                break
            offset += limit

        return playlists

    def get_playlist_tracks(self, playlist_id: str, limit: int = 100) -> List:
        """
        This method is used to get the tracks in a playlist

        Args:
            playlist_id (str): The id of the playlist
            limit (int): The maximum number of items to return

        Returns:
            Any: The return value of the function
        """
        items = []
        offset = 0
        while True:
            response = self._safe_call(
                self.sp.playlist_items, playlist_id, limit=limit, offset=offset
            )

            # Check if the response is valid
            if not response or "items" not in response:
                break

            # Add the items to the list
            items.extend(response["items"])

            # Check if there are more items
            if response["next"] is None:
                break
            offset += 100

        return items

    def get_artists(self, artists_id: List[str]) -> List:
        """
        This method is used to get the artist

        Args:
            artist_id (str): The id of the artist (Max 50)

        Returns:
            Any: The return value of the function
        """
        if len(artists_id) > 50:
            raise Exception("Max 50 artists")

        response = self._safe_call(self.sp.artists, artists_id)
        return response["artists"] if response else []

    def get_tracks(self, tracks_id: List[str]) -> List:
        """
        This method is used to get the track

        Args:
            track_id (str): The id of the track (Max 50)

        Returns:
            Any: The return value of the function
        """
        if len(tracks_id) > 50:
            raise Exception("Max 50 tracks")

        response = self._safe_call(self.sp.tracks)
        return response["tracks"] if response else []

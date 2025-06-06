"""
This class is responsible for consuming the Spotify API
"""

from dataclasses import dataclass
from typing import Any

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

    def get_playlists(self, limit: int = 50) -> dict:
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

    def get_playlist(self, playlist_id: str) -> dict:
        """
        This method is used to get a playlist

        Args:
            playlist_id (str): The id of the playlist

        Returns:
            Any: The return value of the function
        """
        return self._safe_call(self.sp.playlist, playlist_id)

    def get_playlist_tracks(self, playlist_id: str) -> dict:
        """
        This method is used to get the tracks in a playlist

        Args:
            playlist_id (str): The id of the playlist

        Returns:
            Any: The return value of the function
        """
        return self._safe_call(self.sp.playlist_tracks, playlist_id)

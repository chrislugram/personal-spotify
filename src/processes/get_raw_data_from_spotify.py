"""
This file contains the process to get the raw data from spotify
"""

from dataclasses import dataclass, field
from pathlib import Path

from src.processes.process import Process
from src.services.spotify_service import SpotifyService
from src.storage.storage import Storage


@dataclass
class GetRawDataFromSpotify(Process):
    """
    This class is responsible for getting the raw data from spotify
    """

    spotify_service: SpotifyService = field(init=False)
    storage: Storage = field(init=False)

    def __post_init__(self):
        self.spotify_service = SpotifyService(
            client_id=self.settings.environment_settings.SPOTIFY_CLIENT_ID,
            client_secret=self.settings.environment_settings.SPOTIFY_CLIENT_SECRET,
            uri=self.settings.environment_settings.SPOTIFY_URI,
        )
        self.storage = Storage(base_path=self.settings.yaml_settings.storage.base_path)

    def run(self):
        # Get all playlists from spotify
        # For each playlist,
        #     Get all tracks and save to storage
        #     Save playlist to storage
        pass

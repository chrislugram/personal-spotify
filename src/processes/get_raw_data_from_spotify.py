"""
This file contains the process to get the raw data from spotify
"""

import json
from dataclasses import dataclass, field
from datetime import datetime

from src.processes.process import Process
from src.services.spotify.spotify_service import SpotifyService
from src.services.storage.storage import Storage


@dataclass
class GetRawDataFromSpotify(Process):
    """
    This class is responsible for getting the raw data from spotify
    """

    spotify_service: SpotifyService = field(init=False)
    storage: Storage = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.spotify_service = SpotifyService(
            client_id=self.settings.environment_settings.SPOTIFY_CLIENT_ID,
            client_secret=self.settings.environment_settings.SPOTIFY_CLIENT_SECRET,
            uri=self.settings.environment_settings.SPOTIFY_URI,
        )
        self.storage = Storage(base_path=self.settings.yaml_settings.storage.base_path)

    def run(self, execution_date: datetime):
        """
        Run the process
        """
        # Define raw data path
        raw_data_relative_path = (
            self.settings.yaml_settings.storage.raw_zone
            + "/"
            + execution_date.strftime("%Y_%m_%d")
        )

        # Get all playlists from spotify
        playlists = self.spotify_service.get_playlists()
        playlists_bytes = json.dumps(playlists).encode("utf-8")
        self.storage.save(
            relative_path=raw_data_relative_path + "/playlists.json",
            data=playlists_bytes,
        )
        self.logger.info(f"User's Playlists downloaded, total {len(playlists)}")

        # For each playlist,
        #     Get all tracks and save to storage
        #     Save playlist to storage

    def clean(self):
        pass

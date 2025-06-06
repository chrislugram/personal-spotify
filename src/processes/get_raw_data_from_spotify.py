"""
This file contains the process to get the raw data from spotify
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple

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
        playlists = self._get_all_playlists(
            raw_data_relative_path=raw_data_relative_path
        )

        # Get complete tracks for each playlist
        all_artists = set()
        all_tracks = set()
        for playlist in playlists:
            artists, tracks = self._get_tracks_of_playlist(
                playlist_id=playlist["id"],
                playlist_name=playlist["name"],
                raw_data_relative_path=raw_data_relative_path,
            )
            all_artists.update(artists)
            all_tracks.update(tracks)

        # Get all artists from spotify
        self._get_artists(
            artists=all_artists, raw_data_relative_path=raw_data_relative_path
        )

        # Get all tracks from spotify
        self._get_tracks(
            tracks=all_tracks, raw_data_relative_path=raw_data_relative_path
        )

    def _get_artists(self, artists: List[str], raw_data_relative_path: str) -> None:
        """
        Get an artist

        Args:
            artist_id (str): The id of the artist
        """
        artists = []
        for i in range(0, len(artists), 50):
            self.logger.info(f"Getting artists from {i} to {i + 50} of {len(artists)}")
            batch = artists[i : i + 50]
            artists.extend(self.spotify_service.get_artists(artists_id=batch))

        for artist in artists:
            artist_bytes = json.dumps(artist).encode("utf-8")
            self.storage.save(
                relative_path=raw_data_relative_path + f"/artists/{artist['id']}.json",
                data=artist_bytes,
            )

    def _get_tracks(self, tracks: List[str], raw_data_relative_path: str) -> None:
        """
        Get a track

        Args:
            track_id (str): The id of the track
        """
        tracks = []
        for i in range(0, len(tracks), 50):
            self.logger.info(f"Getting tracks from {i} to {i + 50} of {len(tracks)}")
            batch = tracks[i : i + 50]
            tracks.extend(self.spotify_service.get_tracks(tracks_id=batch))

        for track in tracks:
            track_bytes = json.dumps(track).encode("utf-8")
            self.storage.save(
                relative_path=raw_data_relative_path + f"/tracks/{track['id']}.json",
                data=track_bytes,
            )

    def _get_tracks_of_playlist(
        self, playlist_id: str, playlist_name: str, raw_data_relative_path: str
    ) -> Tuple:
        """
        Get all tracks of a playlist

        Args:
            playlist_id (str): The id of the playlist

        Returns:
            Tuple[List[str], List[str]]: The list of artists and tracks
        """
        artists_ids = set()
        tracks_ids = set()

        tracks = self.spotify_service.get_playlist_tracks(playlist_id=playlist_id)
        tracks_bytes = json.dumps(tracks).encode("utf-8")
        self.storage.save(
            relative_path=raw_data_relative_path + f"/playlists/{playlist_id}.json",
            data=tracks_bytes,
        )
        self.logger.info(f"Playlist {playlist_name} downloaded, total {len(tracks)}")

        # TODO: Continue here
        for track in tracks:
            if track is None:
                continue

            if "id" in track["track"].keys():
                tracks_ids.add(track["track"]["id"])
            else:
                self.logger.warning(
                    f"Track {track['track']} does not have an id, skipping..."
                )

            if (
                "artists" in track["track"].keys()
                and len(track["track"]["artists"]) > 0
            ):
                artists_ids.add(track["track"]["artists"][0]["id"])
            else:
                self.logger.warning(
                    f"Track {track['track']} does not have an artist, skipping..."
                )

        return artists_ids, tracks_ids

    def _get_all_playlists(self, raw_data_relative_path: str) -> List:
        """
        Get all playlists

        Args:
            raw_data_relative_path (str): The relative path to the raw data

        Returns:
            list: The list of playlists
        """
        playlists = self.spotify_service.get_playlists()
        playlists_bytes = json.dumps(playlists).encode("utf-8")
        self.storage.save(
            relative_path=raw_data_relative_path + "/playlists.json",
            data=playlists_bytes,
        )
        self.logger.info(f"User's Playlists downloaded, total {len(playlists)}")

        return playlists

    def clean(self):
        pass

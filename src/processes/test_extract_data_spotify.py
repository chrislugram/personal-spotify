import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.processes.extract_data_spotify import GetExtractDataSpotify
from src.services.spotify.spotify_service import SpotifyService
from src.services.storage.storage import Storage


class TestExtractDataSpotify(unittest.TestCase):
    def setUp(self):
        self.settings = MagicMock()
        self.settings.environment_settings = MagicMock()
        self.settings.yaml_settings = MagicMock()
        self.settings.environment_settings.SPOTIFY_CLIENT_ID = "client_id"
        self.settings.environment_settings.SPOTIFY_CLIENT_SECRET = "client_secret"
        self.settings.environment_settings.SPOTIFY_URI = "uri"
        self.settings.yaml_settings.storage.base_path = "/tmp"
        self.settings.yaml_settings.storage.raw_zone = "raw"

        with (
            patch("src.processes.extract_data_spotify.SpotifyService"),
            patch("src.processes.extract_data_spotify.Storage"),
        ):
            self.process = GetExtractDataSpotify(
                name="spotify_raw", settings=self.settings
            )
            self.process.spotify_service = MagicMock(spec=SpotifyService)
            self.process.storage = MagicMock(spec=Storage)

    def test_get_all_playlists(self):
        # Given
        self.process.spotify_service.get_playlists.return_value = [
            {"id": "123", "name": "Test"}
        ]

        # When
        playlists = self.process._get_all_playlists("raw/2025_06_09")

        # Then
        self.assertEqual(len(playlists), 1)
        self.process.storage.save.assert_called_once()

    def test_get_tracks_of_playlist(self):
        # Given
        mock_tracks = [{"track": {"id": "track1", "artists": [{"id": "artist1"}]}}]
        self.process.spotify_service.get_playlist_tracks.return_value = mock_tracks

        # When
        artists, tracks = self.process._get_tracks_of_playlist(
            "id123", "test_playlist", "raw/2025_06_09"
        )

        # Then
        self.assertIn("artist1", artists)
        self.assertIn("track1", tracks)
        self.process.storage.save.assert_called_once()

    def test_get_each_playlist(self):
        # Given
        self.process._get_tracks_of_playlist = MagicMock(
            return_value=({"artist1"}, {"track1"})
        )
        playlists = [{"id": "p1", "name": "Playlist 1"}]

        # When
        artists, tracks = self.process._get_each_playlist(playlists, "raw/2025_06_09")

        # Then
        self.assertEqual(artists, {"artist1"})
        self.assertEqual(tracks, {"track1"})

    def test_get_artists(self):
        # Given
        self.process.spotify_service.get_artists.return_value = [
            {"id": "a1", "name": "Artist"}
        ]

        # When
        self.process._get_artists(["a1"], "raw/2025_06_09")

        # Then
        self.process.spotify_service.get_artists.assert_called_once()
        self.process.storage.save.assert_called_once()

    def test_get_tracks(self):
        # Given
        self.process.spotify_service.get_tracks.return_value = [
            {"id": "t1", "name": "Track"}
        ]

        # When
        self.process._get_tracks(["t1"], "raw/2025_06_09")

        # Then
        self.process.spotify_service.get_tracks.assert_called_once()
        self.process.storage.save.assert_called_once()

    def test_run(self):
        # Given
        self.process._get_all_playlists = MagicMock(
            return_value=[{"id": "1", "name": "test"}]
        )
        self.process._get_each_playlist = MagicMock(return_value=({"a1"}, {"t1"}))
        self.process._get_artists = MagicMock()
        self.process._get_tracks = MagicMock()

        # When
        self.process.run(datetime(2025, 6, 9))

        # Then
        self.process._get_all_playlists.assert_called_once()
        self.process._get_each_playlist.assert_called_once()
        self.process._get_artists.assert_called_once()
        self.process._get_tracks.assert_called_once()

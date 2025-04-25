"""
All tests related to storage
"""

import unittest
from unittest.mock import MagicMock, patch

from src.services.spotify_service import SpotifyService


class TestSpotifyService(unittest.TestCase):
    @patch("src.services.spotify_service.Spotify")
    def test_get_playlists_success(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.current_user_playlists.return_value = {
            "items": [{"name": "Playlist 1", "uri": "spotify:playlist:1"}],
            "next": None,
        }

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        playlists = service.get_playlists()

        # Then
        self.assertIsNotNone(playlists)
        self.assertEqual(len(playlists["items"]), 1)
        self.assertEqual(playlists["items"][0]["name"], "Playlist 1")

    @patch("src.services.spotify_service.Spotify")
    def test_get_playlists_failure(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.current_user_playlists = MagicMock()
        mock_spotify_instance.current_user_playlists.__name__ = "current_user_playlists"
        mock_spotify_instance.current_user_playlists.side_effect = Exception()

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        playlists = service.get_playlists()

        # Then
        self.assertIsNone(playlists)

    @patch("src.services.spotify_service.Spotify")
    def test_get_playlist_success(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.playlist.return_value = {
            "name": "Playlist 1",
            "uri": "spotify:playlist:1",
            "tracks": {"total": 10},
        }

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        playlist = service.get_playlist("spotify:playlist:1")

        # Then
        self.assertIsNotNone(playlist)
        self.assertEqual(playlist["name"], "Playlist 1")
        self.assertEqual(playlist["tracks"]["total"], 10)

    @patch("src.services.spotify_service.Spotify")
    def test_get_playlist_failure(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.playlist = MagicMock()
        mock_spotify_instance.playlist.__name__ = "playlist"
        mock_spotify_instance.playlist.side_effect = Exception()

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        playlist = service.get_playlist("spotify:playlist:1")

        # Then
        self.assertIsNone(playlist)

    @patch("src.services.spotify_service.Spotify")
    def test_get_playlist_tracks_success(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance
        mock_tracks = {
            "items": [
                {"track": {"name": "Song 1", "id": "track1"}},
                {"track": {"name": "Song 2", "id": "track2"}},
            ],
            "total": 2,
        }
        mock_spotify_instance.playlist_tracks.return_value = mock_tracks

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        tracks = service.get_playlist_tracks("spotify:playlist:1")

        # Then
        self.assertIsNotNone(tracks)
        self.assertEqual(len(tracks["items"]), 2)
        self.assertEqual(tracks["items"][0]["track"]["name"], "Song 1")

    @patch("src.services.spotify_service.Spotify")
    def test_get_playlist_tracks_failure(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.playlist_tracks = MagicMock()
        mock_spotify_instance.playlist_tracks.__name__ = "playlist_tracks"
        mock_spotify_instance.playlist_tracks.side_effect = Exception()

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        tracks = service.get_playlist_tracks("spotify:playlist:1")

        # Then
        self.assertIsNone(tracks)

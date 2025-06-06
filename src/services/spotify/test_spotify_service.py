"""
All tests related to storage
"""

import unittest
from unittest.mock import MagicMock, patch

import pytest

from src.services.spotify.spotify_service import SpotifyService


class TestSpotifyService(unittest.TestCase):

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_user_success(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.current_user.return_value = {"id": "user1"}

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        user = service.get_user()

        # Then
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], "user1")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_playlists_success_without_next(self, MockSpotify):
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
        self.assertEqual(len(playlists), 1)
        self.assertEqual(playlists[0]["name"], "Playlist 1")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_playlists_success_with_next(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.current_user_playlists.side_effect = [
            {
                "items": [
                    {"name": "Playlist 1", "uri": "spotify:playlist:1"},
                ],
                "next": "next_page",
            },
            {
                "items": [
                    {"name": "Playlist 2", "uri": "spotify:playlist:2"},
                ],
                "next": None,
            },
        ]

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        playlists = service.get_playlists(limit=1)

        # Then
        self.assertIsNotNone(playlists)
        self.assertEqual(len(playlists), 2)
        self.assertEqual(playlists[0]["name"], "Playlist 1")
        self.assertEqual(playlists[1]["name"], "Playlist 2")

    @patch("src.services.spotify.spotify_service.Spotify")
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
        self.assertEqual(playlists, [])

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_playlist_tracks_success_without_next(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.playlist_items.return_value = {
            "items": [{"name": "Track 1", "uri": "spotify:track:1"}],
            "next": None,
        }

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        tracks = service.get_playlist_tracks("playlist_id")

        # Then
        self.assertIsNotNone(tracks)
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0]["name"], "Track 1")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_playlist_tracks_success_with_next(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.playlist_items.side_effect = [
            {
                "items": [
                    {"name": "Track 1", "uri": "spotify:track:1"},
                ],
                "next": "next_page",
            },
            {
                "items": [
                    {"name": "Track 2", "uri": "spotify:track:2"},
                ],
                "next": None,
            },
        ]

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )

        tracks = service.get_playlist_tracks("playlist_id", limit=1)

        # Then
        self.assertIsNotNone(tracks)
        self.assertEqual(len(tracks), 2)
        self.assertEqual(tracks[0]["name"], "Track 1")
        self.assertEqual(tracks[1]["name"], "Track 2")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_playlist_tracks_failure(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.playlist_items = MagicMock()
        mock_spotify_instance.playlist_items.__name__ = "playlist_items"
        mock_spotify_instance.playlist_items.side_effect = Exception()

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        tracks = service.get_playlist_tracks("playlist_id")

        # Then
        self.assertEqual(tracks, [])

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_artists_success(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.artists.return_value = {"artists": [{"name": "Artist 1"}]}

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        artists = service.get_artists(["artist_id"])

        # Then
        self.assertIsNotNone(artists)
        self.assertEqual(len(artists), 1)
        self.assertEqual(artists[0]["name"], "Artist 1")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_artists_more_than_50(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        artists = []
        for i in range(51):
            artists.append({"name": f"Artist {i}"})
        mock_spotify_instance.artists.return_value = {"artists": artists}

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        with pytest.raises(Exception) as exc:
            artists = service.get_artists(artists)

        # Then
        self.assertEqual(str(exc.value), "Max 50 artists")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_artists_failure(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.artists = MagicMock()
        mock_spotify_instance.artists.__name__ = "artists"
        mock_spotify_instance.artists.side_effect = Exception()

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        artists = service.get_artists(["artist_id"])

        # Then
        self.assertEqual(artists, [])

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_tracks_success(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.tracks.return_value = {"tracks": [{"name": "Track 1"}]}

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        tracks = service.get_tracks(["track_id"])

        # Then
        self.assertIsNotNone(tracks)
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0]["name"], "Track 1")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_tracks_more_than_50(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        tracks = []
        for i in range(51):
            tracks.append({"name": f"tracks {i}"})
        mock_spotify_instance.tracks.return_value = {"tracks": tracks}

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        with pytest.raises(Exception) as exc:
            tracks = service.get_tracks(tracks)

        # Then
        self.assertEqual(str(exc.value), "Max 50 tracks")

    @patch("src.services.spotify.spotify_service.Spotify")
    def test_get_tracks_failure(self, MockSpotify):
        # Given
        mock_spotify_instance = MagicMock()
        MockSpotify.return_value = mock_spotify_instance

        mock_spotify_instance.tracks = MagicMock()
        mock_spotify_instance.tracks.__name__ = "tracks"
        mock_spotify_instance.tracks.side_effect = Exception()

        # When
        service = SpotifyService(
            client_id="test_client_id",
            client_secret="test_client_secret",
            uri="test_uri",
        )
        tracks = service.get_tracks(["tracks_id"])

        # Then
        self.assertEqual(tracks, [])

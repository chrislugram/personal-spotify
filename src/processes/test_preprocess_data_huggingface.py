import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.processes.preprocess_data_huggingface import PreprocessDataHugginface
from src.services.storage.storage import Storage


class TestPreprocessDataHuggingface(unittest.TestCase):

    def setUp(self):
        self.settings = MagicMock()
        self.settings.yaml_settings = MagicMock()
        self.settings.yaml_settings.storage.base_path = "/tmp"
        self.settings.yaml_settings.storage.raw_zone = "raw"
        self.settings.yaml_settings.storage.processed_zone = "processed"

        with patch("src.processes.preprocess_data_huggingface.Storage"):
            self.process = PreprocessDataHugginface(
                name="huggingface_processed", settings=self.settings
            )
            self.process.storage = MagicMock(spec=Storage)

    def test_get_common_columns(self):
        # Given
        df_maharshipandya = pd.DataFrame(
            {"column1": [1, 2, 3], "column2": [4, 5, 6], "Unnamed: 0": [7, 8, 9]}
        )
        df_khepplewhite = pd.DataFrame(
            {"column1": [7, 8, 9], "column2": [10, 11, 12], "Unnamed: 0": [7, 8, 9]}
        )
        expected_output = {"column1", "column2", "track_id", "artists"}

        # When
        common_columns = self.process._get_common_columns(
            df_maharshipandya, df_khepplewhite
        )

        # Then
        self.assertEqual(common_columns, expected_output)

    def test_refactor_artists_namees(self):
        # Given
        artist_names = "artist1, artist2, artist3"
        expected_output = "artist1;artist2;artist3"

        # When
        result = self.process._refactor_artists_namees(artist_names)

        # Then
        self.assertEqual(result, expected_output)

    def test_refactor_astists_namees_empty(self):
        # Given
        artist_names = ""
        expected_output = ""

        # When
        result = self.process._refactor_artists_namees(artist_names)

        # Then
        self.assertEqual(result, expected_output)

    def test_preprocess_maharshipandya(self):
        # Given
        common_columns = {"track_id", "artists"}
        df_maharshipandya = pd.DataFrame(
            {
                "track_id": [1, 2, 3],
                "artists": [4, 5, 6],
                "duration_ms": [7, 8, 9],
                "explicit": [10, 11, 12],
                "track_genre": [13, 14, 15],
                "Unnamed: 0": [7, 8, 9],
            }
        )
        expected_output = pd.DataFrame(
            {
                "track_id": [1, 2, 3],
                "artists": [4, 5, 6],
                "duration_ms": [7, 8, 9],
                "explicit": [10, 11, 12],
                "track_genre": [13, 14, 15],
            }
        )

        # When
        result = self.process._preprocess_maharshipandya(
            df_maharshipandya, common_columns
        )

        # Then
        self.assertEqual(result.shape, expected_output.shape)
        self.assertEqual(len(result.columns), len(expected_output.columns))
        self.assertEqual(set(result.columns), set(expected_output.columns))

    def test_preprocess_khepplewhite(self):
        # Given
        common_columns = {"track_id", "artists"}
        df_khepplewhite = pd.DataFrame(
            {
                "uri": ["aaaa:t1", "bbbb:t3", "cccc:t2"],
                "artist_names": [
                    "artist1, artist2, artist3",
                    "artist1, artist2",
                    "artist1",
                ],
                "language": ["es", "en", "es"],
                "Unnamed: 0": [7, 8, 9],
            }
        )
        expected_output = pd.DataFrame(
            {
                "track_id": ["t1", "t2", "t3"],
                "artists": ["artist1;artist2;artist3", "artist1;artist2", "artist1"],
                "language": ["es", "en", "es"],
            }
        )

        # When
        result = self.process._preprocess_khepplewhite(df_khepplewhite, common_columns)

        # Then
        self.assertEqual(result.shape, expected_output.shape)
        self.assertEqual(len(result.columns), len(expected_output.columns))
        self.assertEqual(set(result.columns), set(expected_output.columns))
        self.assertEqual(
            set(result["track_id"].tolist()), set(expected_output["track_id"].tolist())
        )
        self.assertEqual(
            set(result["artists"].tolist()), set(expected_output["artists"].tolist())
        )
        self.assertEqual(
            set(result["language"].tolist()), set(expected_output["language"].tolist())
        )

    def test_merge_dataframes(self):
        # Given
        df_maharshipandya = pd.DataFrame(
            {"track_id": [1, 2, 3, 4], "column2": [4, 5, 6, 7]}
        )
        df_khepplewhite = pd.DataFrame(
            {
                "track_id": [7, 8, 9, 4],
                "column2": [10, 11, 12, 13],
                "other_column": [7, 8, 9, 10],
            }
        )
        expected_output = pd.DataFrame(
            {
                "track_id": [1, 2, 3, 4, 7, 8, 9],
                "column2": [4, 5, 6, 7, 10, 11, 12],
                "other_column": [None, None, None, 7, 8, 9, 10],
            }
        )

        # When
        result = self.process._merge_dataframes(df_maharshipandya, df_khepplewhite)

        # Then
        self.assertEqual(result.shape, expected_output.shape)
        self.assertEqual(len(result.columns), len(expected_output.columns))
        self.assertEqual(set(result.columns), set(expected_output.columns))

        # Check that the input DataFrames have the expected columns
        self.assertIn("track_id", df_maharshipandya.columns)
        self.assertIn("column2", df_maharshipandya.columns)
        self.assertIn("track_id", df_khepplewhite.columns)
        self.assertIn("column2", df_khepplewhite.columns)
        self.assertIn("other_column", df_khepplewhite.columns)

        # Check that the merged DataFrame has the expected columns
        self.assertIn("track_id", result.columns)
        self.assertIn("column2", result.columns)
        self.assertIn("other_column", result.columns)

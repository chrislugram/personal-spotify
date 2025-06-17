import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd

from src.processes.extract_data_huggingface import ExtractDataHuggingFace
from src.services.storage.storage import Storage


class TestExtractDataHuggingFace(unittest.TestCase):
    def setUp(self):
        # Mock settings

        self.settings = MagicMock()
        self.settings.yaml_settings = MagicMock()
        self.settings.yaml_settings.storage = MagicMock()
        self.settings.yaml_settings.huggingface = MagicMock()
        self.settings.yaml_settings.huggingface.maharshipandya = (
            "fake_maharshipandya.csv"
        )
        self.settings.yaml_settings.huggingface.khepplewhite = "fake_khepplewhite.csv"
        self.settings.yaml_settings.storage.base_path = "/tmp"
        self.settings.yaml_settings.storage.raw_zone = "raw"

        with patch("src.processes.extract_data_huggingface.Storage"):
            self.process = ExtractDataHuggingFace(
                name="huggingface_raw", settings=self.settings
            )
            self.process.storage = MagicMock(spec=Storage)

    @patch("pandas.read_csv")
    def test_get_raw_data_huggingface_reads_csv(self, mock_read_csv):
        # Givenn
        df_mock = pd.DataFrame({"col": [1, 2]})
        mock_read_csv.return_value = df_mock

        # Then
        df1, df2 = self.process._get_raw_data_huggingface()

        self.assertIsInstance(df1, pd.DataFrame)
        self.assertIsInstance(df2, pd.DataFrame)
        self.assertEqual(mock_read_csv.call_count, 2)
        mock_read_csv.assert_any_call("fake_maharshipandya.csv")
        mock_read_csv.assert_any_call("fake_khepplewhite.csv")

    @patch("pandas.read_csv", side_effect=Exception("Read error"))
    def test_get_raw_data_huggingface_logs_and_raises(self, mock_read_csv):
        # Given
        # When
        with self.assertRaises(Exception) as cm:
            self.process._get_raw_data_huggingface()

        # Then
        self.assertEqual(str(cm.exception), "Read error")

    @patch.object(ExtractDataHuggingFace, "_get_raw_data_huggingface")
    def test_run_calls_save_dataframe(self, mock_get_data):
        # Given
        df1 = pd.DataFrame({"a": [1]})
        df2 = pd.DataFrame({"b": [2]})
        mock_get_data.return_value = (df1, df2)
        execution_date = datetime(2023, 4, 1)
        base_path = "raw/2023_04_01"

        # When
        self.process.run(execution_date)

        # Then
        calls = self.process.storage.save_dataframe.call_args_list

        self.assertEqual(self.process.storage.save_dataframe.call_count, 2)

        self.assertEqual(
            calls[0].kwargs["relative_path"], f"{base_path}/maharshipandya.parquet"
        )
        pd.testing.assert_frame_equal(calls[0].kwargs["dataframe"], df1)

        self.assertEqual(
            calls[1].kwargs["relative_path"], f"{base_path}/khepplewhite.parquet"
        )
        pd.testing.assert_frame_equal(calls[1].kwargs["dataframe"], df2)

"""
This module is used to extract data from huggingface
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple

import pandas as pd

from src.processes.process import Process
from src.services.storage.storage import Storage


@dataclass
class ExtractDataHuggingFace(Process):
    """
    This class is used to extract data from huggingface
    """

    storage: Storage = field(init=False)

    def __post_init__(self):
        super().__post_init__()
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

        # Get dataframes from huggingface
        df_maharshipandya, df_khepplewhite = self._get_raw_data_huggingface()

        # Save in storage
        self.storage.save_dataframe(
            relative_path=raw_data_relative_path + "/maharshipandya.parquet",
            dataframe=df_maharshipandya,
        )

        self.storage.save_dataframe(
            relative_path=raw_data_relative_path + "/khepplewhite.parquet",
            dataframe=df_khepplewhite,
        )

    def clean(self):
        return super().clean()

    def _get_raw_data_huggingface(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get raw data from huggingface

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Tuple of dataframes
        """
        try:
            df_maharshipandya = pd.read_csv(
                self.settings.yaml_settings.huggingface.maharshipandya
            )

            df_khepplewhite = pd.read_csv(
                self.settings.yaml_settings.huggingface.khepplewhite
            )

            return df_maharshipandya, df_khepplewhite
        except Exception as e:
            self.logger.error(f"Error getting data from huggingface: {e}")
            raise e

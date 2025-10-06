"""
This module is used to preprocess data from huggingface
"""

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

from src.processes.process import Process
from src.services.storage.storage import Storage


@dataclass
class PreprocessDataHugginface(Process):
    """
    This class is used to preprocess data from huggingface
    """

    storage: Storage = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.storage = Storage(base_path=self.settings.yaml_settings.storage.base_path)

    def run(self, execution_date: datetime):
        """
        Run the process
        """
        # Prepare relative paths
        raw_data_relative_path = (
            self.settings.yaml_settings.storage.raw_zone
            + "/"
            + execution_date.strftime("%Y_%m_%d")
        )
        processed_data_relative_path = (
            self.settings.yaml_settings.storage.processed_zone
            + "/"
            + execution_date.strftime("%Y_%m_%d")
        )

        # Read dataframes from storage
        df_maharshipandya = self.storage.load_dataframe(
            raw_data_relative_path + "/maharshipandya.parquet"
        )
        df_khepplewhite = self.storage.load_dataframe(
            raw_data_relative_path + "/khepplewhite.parquet"
        )

        # Create common columns from dataframes
        common_columns = self._get_common_columns(df_maharshipandya, df_khepplewhite)

        # Preprocess maharshipandya
        df_maharshipandya = self._preprocess_maharshipandya(
            df_maharshipandya, common_columns
        )

        # Preprocess khepplewhite
        df_khepplewhite = self._preprocess_khepplewhite(df_khepplewhite, common_columns)

        # Merge dataframes
        df_maharshipandya = self._merge_dataframes(df_maharshipandya, df_khepplewhite)

        # Save in storage
        self.storage.save_dataframe(
            relative_path=processed_data_relative_path + "/huggingface.parquet",
            dataframe=df_maharshipandya,
        )

    def clean(self):
        return super().clean()

    def _merge_dataframes(
        self, df_maharshipandya: pd.DataFrame, df_khepplewhite: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge dataframes

        Args:
            df_maharshipandya (pd.DataFrame): Maharshipandya dataframe
            df_khepplewhite (pd.DataFrame): Khepplewhite dataframe

        Returns:
            pd.DataFrame: Merged dataframe
        """
        # Merge the two dataframes on the "track_id" column
        merged_df = pd.merge(
            df_maharshipandya,
            df_khepplewhite,
            on="track_id",
            how="outer",
            suffixes=("_1", "_2"),
        )
        for col in df_maharshipandya.columns.intersection(df_khepplewhite.columns):
            if col != "track_id":
                merged_df[col] = merged_df[f"{col}_1"].combine_first(
                    merged_df[f"{col}_2"]
                )
                merged_df = merged_df.drop(columns=[f"{col}_1", f"{col}_2"])

        # Get the common columns between the two dataframes
        common_columns = set(df_maharshipandya.columns) & set(df_khepplewhite.columns)

        # Get the unique columns from each dataframe
        unique_columns_maharshipandya = set(df_maharshipandya.columns) - common_columns
        unique_columns_khepplewhite = set(df_khepplewhite.columns) - common_columns

        # Combine the columns in the desired order
        all_columns = (
            list(common_columns)
            + list(unique_columns_maharshipandya)
            + list(unique_columns_khepplewhite)
        )

        # Reorder the columns of the merged dataframe
        merged_df = merged_df[all_columns]

        return merged_df

    def _get_common_columns(
        self, df_maharshipandya: pd.DataFrame, df_khepplewhite: pd.DataFrame
    ) -> set[str]:
        """
        Get common columns from dataframes

        Args:
            df_maharshipandya (pd.DataFrame): Maharshipandya dataframe
            df_khepplewhite (pd.DataFrame): Khepplewhite dataframe

        Returns:
            pd.DataFrame: Common columns dataframe
        """
        common_columns = set(df_maharshipandya.columns).intersection(
            set(df_khepplewhite.columns)
        )
        common_columns.remove("Unnamed: 0")
        common_columns.add("track_id")
        common_columns.add("artists")

        return common_columns

    def _preprocess_khepplewhite(
        self, df_khepplewhite: pd.DataFrame, common_columns: set[str]
    ) -> pd.DataFrame:
        """
        Preprocess dataframe for extra information

        Args:
            df_khepplewhite (pd.DataFrame): khepplewhite dataframe
            columns (set[str]): List of columns

        Returns:
            pd.DataFrame: Preprocessed khepplewhite dataframe
        """
        # Add track_id column
        df_khepplewhite["track_id"] = df_khepplewhite["uri"].str.split(":").str[-1]

        # Add artists column
        df_khepplewhite["artists"] = df_khepplewhite["artist_names"].apply(
            self._refactor_artists_namees
        )

        # Get only relevant columns
        columns_for_khepplewhite = common_columns.copy()
        columns_for_khepplewhite.add("language")
        return df_khepplewhite[list(columns_for_khepplewhite)]

    def _preprocess_maharshipandya(
        self, df_maharshipandya: pd.DataFrame, common_columns: set[str]
    ) -> pd.DataFrame:
        """
        Preprocess dataframe for extra information

        Args:
            df_maharshipandya (pd.DataFrame): Maharshipandya dataframe
            columns (set[str]): List of columns

        Returns:
            pd.DataFrame: Preprocessed Maharshipandya dataframe
        """
        colums_for_maharshipandya = common_columns.copy()
        colums_for_maharshipandya.add("duration_ms")
        colums_for_maharshipandya.add("explicit")
        colums_for_maharshipandya.add("track_genre")
        return df_maharshipandya[list(colums_for_maharshipandya)]

    def _refactor_artists_namees(self, artist_names: str) -> str:
        """
        Refactor artist names

        Args:
            artist_names (str): Artist names

        Returns:
            str: Refactored artist names
        """
        split_names = artist_names.split(", ")
        return ";".join(split_names)

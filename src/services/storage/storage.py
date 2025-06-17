"""
This class is the main class for the storage of the data
"""

from io import BytesIO
from typing import List

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from cloudpathlib import AnyPath


class Storage:

    def __init__(self, base_path: str):
        self.base_path = AnyPath(base_path)

    def _absolute_path(self, path: str) -> AnyPath:
        """
        Returns the absolute path

        Args:
            path (str): The path to the file

        Returns:
            CloudPath: The absolute path
        """
        return self.base_path / path

    def save(self, relative_path: str, data: bytes):
        """
        Save the data in the storage

        Args:
            relative_path (str): The relative path to the file
            data (bytes): The data to save
        """
        complete_path = self._absolute_path(relative_path)
        complete_path.parent.mkdir(parents=True, exist_ok=True)
        complete_path.write_bytes(data)

    def save_dataframe(self, relative_path: str, dataframe):
        """
        Save the dataframe in the storage

        Args:
            relaative_path (str): The relative path to the file
            dataframe (pd.DataFrame): The dataframe to save
        """
        buffer = BytesIO()
        table = pa.Table.from_pandas(dataframe)
        pq.write_table(table, buffer)
        buffer.seek(0)
        self.save(relative_path, buffer.read())

    def load(self, relative_path: str) -> bytes:
        """
        Load the data from the storage

        Args:
            relative_path (str): The relative path to the file

        Returns:
            bytes: The data
        """
        return self._absolute_path(relative_path).read_bytes()

    def load_dataframe(self, relative_path: str) -> pd.DataFrame:
        """
        Load the dataframe from the storage

        Args:
            relative_path (str): The relative path to the file

        Returns:
            pd.DataFrame: The dataframe
        """
        buffer = BytesIO(self.load(relative_path))
        table = pq.read_table(buffer)
        return table.to_pandas()

    def exists(self, relative_path: str) -> bool:
        """
        Check if the file exists

        Args:
            relative_path (str): The relative path to the file

        Returns:
            bool: True if the file exists
        """
        return self._absolute_path(relative_path).exists()

    def delete(self, relative_path: str):
        """
        Delete the file

        Args:
            relative_path (str): The relative path to the file
        """
        complete_path = self._absolute_path(relative_path)
        if complete_path.exists():
            if complete_path.is_dir():
                for file in complete_path.iterdir():
                    file.unlink()
                complete_path.rmdir()
            elif complete_path.is_file():
                complete_path.unlink()

    def list_files(self, relative_path: str) -> List[str]:
        """
        List the files in the directory

        Args:
            relative_path (str): The relative path to the directory

        Returns:
            List[str]: The list of files
        """
        complete_path = self._absolute_path(relative_path)
        if not complete_path.exists():
            return []

        return [str(p.relative_to(complete_path)) for p in complete_path.iterdir()]

"""
All tests related to storage
"""

import shutil
import unittest
from pathlib import Path

from cloudpathlib import AnyPath

from src.storage.storage import Storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.base_path = Path.cwd() / "test_base_path"

    def tearDown(self):
        shutil.rmtree(self.base_path, ignore_errors=True)

    def test_init(self):
        # Given base path
        # When creating storage
        storage = Storage(self.base_path)

        # Then base path is set
        self.assertEqual(storage.base_path, AnyPath(self.base_path))

    def test_absolute_path(self):
        # Given
        storage = Storage(self.base_path)

        # When
        relative_path = "test_relative_path"
        expected_absolute_path = AnyPath(self.base_path) / relative_path

        # Then
        self.assertEqual(storage._absolute_path(relative_path), expected_absolute_path)

    def test_save(self):
        # Given
        storage = Storage(self.base_path)
        relative_path = "test_relative_path.txt"
        data = b"test_data"

        # When
        storage.save(relative_path, data)

        # Then
        file_path = self.base_path / relative_path
        self.assertTrue(file_path.exists())

        file_content = file_path.read_bytes()
        self.assertEqual(file_content, data)

    def test_save_non_bytes_data(self):
        # Given
        storage = Storage(self.base_path)
        relative_path = "test_relative_path.txt"
        data = "test_data"  # not bytes

        # When
        with self.assertRaises(TypeError):
            storage.save(relative_path, data)

    def test_delete(self):
        # Given
        self.base_path.mkdir(parents=True, exist_ok=True)
        storage = Storage(self.base_path)
        relative_file = self.base_path / "test_relative_path.txt"
        relative_file.touch(exist_ok=True)

        # When
        storage.delete(relative_file)

        # Then
        self.assertFalse(relative_file.exists())

    def test_delete_with_parents(self):
        # Given
        self.base_path.mkdir(parents=True, exist_ok=True)
        storage = Storage(self.base_path)
        relative_folder = self.base_path / "test_relative_path"
        relative_folder.mkdir(parents=True, exist_ok=True)
        relative_file = relative_folder / "test_relative_path.txt"
        relative_file.touch(exist_ok=True)

        # When
        storage.delete(relative_folder)

        # Then
        self.assertFalse(relative_file.exists())

    def test_exists(self):
        # Given
        self.base_path.mkdir(parents=True, exist_ok=True)
        storage = Storage(self.base_path)
        relative_file = self.base_path / "test_relative_path.txt"
        relative_file.touch(exist_ok=True)

        # When
        exists = storage.exists(relative_file)

        # Then
        self.assertTrue(exists)

    def test_load(self):
        # Given
        self.base_path.mkdir(parents=True, exist_ok=True)
        storage = Storage(self.base_path)
        relative_file = self.base_path / "test_relative_path.txt"
        relative_file.write_bytes(b"test_data")

        # When
        data = storage.load(relative_file)

        # Then
        self.assertEqual(data, b"test_data")

    def test_list_files(self):
        # Given
        self.base_path.mkdir(parents=True, exist_ok=True)
        storage = Storage(self.base_path)
        relative_folder = self.base_path / "test_relative_path"
        relative_folder.mkdir(parents=True, exist_ok=True)
        relative_file = relative_folder / "test_relative_path.txt"
        relative_file.touch(exist_ok=True)

        # When
        files = storage.list_files(relative_folder)

        # Then
        self.assertEqual(files, ["test_relative_path.txt"])

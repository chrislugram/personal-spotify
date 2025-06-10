run-tests:
	poetry run pytest -vv -s src/services/storage/test_storage.py
	poetry run pytest -vv -s src/services/spotify/test_spotify_service.py
	poetry run pytest -vv -s src/processes/test_get_raw_data_from_spotify.py

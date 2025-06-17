run-tests:
	poetry run pytest -vv -s src/services/storage/test_storage.py
	poetry run pytest -vv -s src/services/spotify/test_spotify_service.py
	poetry run pytest -vv -s src/processes/test_extract_data_spotify.py
	poetry run pytest -vv -s src/processes/test_extract_data_huggingface.py

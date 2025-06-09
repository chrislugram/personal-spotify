from src.config.settings import Settings
from src.pipelines.ingest_music_data import IngestMusicData


def main():
    settings = Settings()
    pipeline = IngestMusicData(name="ingest_music_data", settings=settings)
    pipeline.execute()


if __name__ == "__main__":
    main()

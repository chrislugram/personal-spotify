from src.pipelines.pipeline import Pipeline
from src.processes.extract_data_spotify import ExtractDataSpotify


class IngestMusicData(Pipeline):
    def initialize(self):
        # Create list of steps process
        self.processes = [
            ExtractDataSpotify(
                name="get_raw_data_from_spotify", settings=self.settings
            ),
        ]

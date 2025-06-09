from src.pipelines.pipeline import Pipeline
from src.processes.get_raw_data_from_spotify import GetRawDataFromSpotify


class IngestMusicData(Pipeline):
    def initialize(self):
        # Create list of steps process
        self.processes = [
            GetRawDataFromSpotify(
                name="get_raw_data_from_spotify", settings=self.settings
            ),
        ]

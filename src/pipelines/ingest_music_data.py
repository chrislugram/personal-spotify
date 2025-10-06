from src.pipelines.pipeline import Pipeline
from src.processes.extract_data_huggingface import ExtractDataHuggingFace
from src.processes.extract_data_spotify import ExtractDataSpotify
from src.processes.preprocess_data_huggingface import PreprocessDataHugginface


class IngestMusicData(Pipeline):
    def initialize(self):
        # Create list of steps process
        self.processes = [
            ExtractDataSpotify(
                name="get_raw_data_from_spotify", settings=self.settings
            ),
            ExtractDataHuggingFace(
                name="get_raw_data_from_huggingface", settings=self.settings
            ),
            PreprocessDataHugginface(
                name="preprocess_data_huggingface", settings=self.settings
            ),
        ]

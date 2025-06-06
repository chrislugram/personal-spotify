"""
This is a base class for pipelines
Later will be change for an orchectrator
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from src.config.settings import Settings
from src.processes.process import Process


@dataclass
class Pipeline(ABC):
    name: str
    settings: Settings
    processes: List[Process] = field(init=False)
    logger: logging.Logger = field(init=False)

    def __post_init__(self):
        self.logger = logging.getLogger(self.name)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f"%(asctime)s - {self.name} - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.initialize()

    @abstractmethod
    def initialize(self):
        """
        Initialize the pipeline, create steps here
        """
        pass

    def execute(self):
        """
        Execute the list of process
        """
        for process in self.processes:
            self.logger.info(f"Running {process.name}")
            process.run()

            self.logger.info(f"Cleaning {process.name}")
            process.clean()

"""
This class is a base class for all processes
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Process(ABC):
    name: str
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

    @abstractmethod
    def run(self):
        """
        Run the process
        """
        pass

    @abstractmethod
    def clean(self):
        """
        Clean the process
        """
        pass

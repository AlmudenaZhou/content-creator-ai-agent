import os
import logging
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)

class BaseReader(ABC):

    @abstractmethod
    @staticmethod
    def read(file_path: str) -> str:
        """
        Reads a file and returns its content.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The raw content of the file.
        """
        pass
    
    @staticmethod
    def _get_folder_hierarchy(file_path: str) -> tuple[list[str], str]:
        file_folder_hierarchy, filename = os.path.split(file_path)
        folder_hierarchy = file_folder_hierarchy.split(os.sep)

        logger.info("Extracted folder hierarchy from markdown file")
        return folder_hierarchy, filename

    @abstractmethod
    @staticmethod
    def read_with_metadata(file_path: str) -> dict:
        """
        Reads a file and returns its content along with folder metadata.

        Args:
            file_path (str): The path to the file.

        Returns:
            dict: A dictionary containing the raw content and folder metadata.
        """

        return {
            "title": "",
            "raw_content": "",
            "folders": ""
        }

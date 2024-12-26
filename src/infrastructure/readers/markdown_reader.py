import logging

from src.infrastructure.readers import BaseReader


logger = logging.getLogger(__name__)

class MarkdownReader(BaseReader):

    @staticmethod
    def read(file_path: str) -> str:
        """
        Reads a Markdown file and returns its content as a string.

        Args:
            file_path (str): The path to the Markdown file.

        Returns:
            str: The raw content of the Markdown file.
        """

        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        logger.info(f"Read markdown file: {file_path}")
        return markdown_content

    @staticmethod
    def read_with_metadata(file_path: str) -> dict:
        """
        Reads a Markdown file and returns its content along with folder metadata.

        Args:
            file_path (str): The path to the Markdown file.

        Returns:
            dict: A dictionary containing the raw content and folder metadata.
        """
        logger.info(f"Processing file: {file_path}")

        if not file_path.endswith(".md"):
            logger.warning("The file extension is not .md")

        markdown_content = MarkdownReader.read(file_path)
        folder_hierarchy, filename = MarkdownReader._get_folder_hierarchy(file_path)

        logger.info("Extracted folder hierarchy from markdown file")
        return {
            "title": filename.replace(".md", ""),
            "raw_content": markdown_content,
            "folders": folder_hierarchy
        }

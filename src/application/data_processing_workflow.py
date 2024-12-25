import os
import json
import logging

from src.infrastructure.readers import MarkdownReader
from src.infrastructure.writers import JsonWriter
from src.domain.data_processing import ObsidianMarkdownProcessor


logger = logging.getLogger(__name__)

class DataProcessingWorkflow:

    @staticmethod
    def process_markdown_file(input_path: str, output_path: str) -> None:
        """
        Coordinates the processing of a Markdown file.

        Args:
            input_path (str): Path to the Markdown file.
            output_path (str): Path to save the processed JSON output.
        """
        md_content = MarkdownReader.read_with_metadata(input_path)

        document = ObsidianMarkdownProcessor.process(md_content)

        JsonWriter.write(json.loads(document.json()), output_path)

    @staticmethod
    def process_directory(input_dir: str, output_dir: str) -> None:
        """
        Processes all Markdown files in a directory.

        Args:
            input_dir (str): Directory containing Markdown files.
            output_dir (str): Directory to save the processed JSON files.
        """

        os.makedirs(output_dir, exist_ok=True)
        for root, _, files in os.walk(input_dir):

            logger.info(f"Checking for md files in folder: {root}")
            relative_path = os.path.relpath(root, input_dir)

            current_output_dir = os.path.join(output_dir, relative_path)
            os.makedirs(current_output_dir, exist_ok=True)

            for file_name in files:
                if file_name.endswith(".md"):
                    logger.info(f"Starting process with file: {file_name}")
                    input_path = os.path.join(root, file_name)
                    output_path = os.path.join(current_output_dir, f"{file_name}.json")
                    DataProcessingWorkflow.process_markdown_file(input_path, output_path)

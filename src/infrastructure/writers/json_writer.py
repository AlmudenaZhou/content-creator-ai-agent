import json
from typing import Union

class JsonWriter:
    @staticmethod
    def write(data: Union[dict, list], output_path: str) -> None:
        """
        Writes JSON data to a file.

        Args:
            data (dict): The JSON data to write.
            output_path (str): The path to the output file.
        """
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

import json
import sys

from logger import logger


def read_from_json(file_path: str):
    try:
        with open(file_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Encountered an unexpected error while reading a JSON file '{file_path}': {e}.")
        sys.exit(1)

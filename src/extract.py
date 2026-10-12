import pandas as pd
import requests
from src.logger import setup_logger

logger = setup_logger()

class DataExtractor:
    def __init__(self, config: dict):
        self.config = config

    def extract_csv(self) -> pd.DataFrame:
        path = self.config["sources"]["csv_path"]
        logger.info(f"Extracting data from CSV: {path}")
        return pd.read_csv(path)

    def extract_json(self) -> pd.DataFrame:
        path = self.config["sources"]["json_path"]
        logger.info(f"Extracting data from JSON: {path}")
        return pd.read_json(path)

    def extract_api(self) -> pd.DataFrame:
        url = self.config["sources"]["api_url"]
        logger.info(f"Fetching data from API endpoint: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())

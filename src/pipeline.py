import yaml
from pathlib import Path
from src.extract import DataExtractor
from src.transform import DataTransformer
from src.logger import setup_logger

logger = setup_logger()

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_pipeline():
    logger.info("=== Pipeline Execution Started ===")
    config = load_config()

    # Step 1: Extract
    extractor = DataExtractor(config)
    try:
        df = extractor.extract_csv()  # Switch to extract_json() or extract_api() as needed
    except Exception as e:
        logger.critical(f"Pipeline failed during extraction stage: {e}")
        return

    # Step 2: Transform
    transformer = DataTransformer(config)
    try:
        transformed_df = transformer.clean_data(df)
    except Exception as e:
        logger.critical(f"Pipeline failed during transformation stage: {e}")
        return

    # Step 3: Load
    output_path = Path(config["destinations"]["output_csv"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        transformed_df.to_csv(output_path, index=False)
        logger.info(f"Successfully wrote output to {output_path}")
    except Exception as e:
        logger.critical(f"Pipeline failed during load stage: {e}")
        return

    logger.info("=== Pipeline Execution Completed Successfully ===")

if __name__ == "__main__":
    run_pipeline()
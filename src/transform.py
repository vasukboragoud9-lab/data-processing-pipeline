import pandas as pd
from src.logger import setup_logger

logger = setup_logger()

class DataTransformer:
    def __init__(self, config: dict):
        self.config = config.get("transformations", {})

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Starting data cleaning and transformation process...")
        initial_count = len(df)

        # 1. Handle Duplicates
        if self.config.get("drop_duplicates", True):
            df = df.drop_duplicates()
            logger.info(f"Dropped {initial_count - len(df)} duplicate rows.")

        # 2. Type Conversions & Missing Values for Numeric Columns
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                strategy = self.config.get("numeric_imputation", "mean")
                if strategy == "mean":
                    fill_val = df[col].mean()
                elif strategy == "median":
                    fill_val = df[col].median()
                else:
                    fill_val = 0
                df[col] = df[col].fillna(fill_val)
                logger.info(f"Imputed {missing_count} missing values in numeric column '{col}' with {strategy} ({fill_val}).")

        # 3. Type Conversions & Missing Values for Categorical Columns
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in categorical_cols:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                fill_val = self.config.get("categorical_imputation", "Unknown")
                df[col] = df[col].fillna(fill_val).astype(str)
                logger.info(f"Imputed {missing_count} missing values in categorical column '{col}' with '{fill_val}'.")

        # 4. Date Parsing Edge Cases
        date_cols = self.config.get("date_columns", [])
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                invalid_dates = df[col].isnull().sum()
                if invalid_dates > 0:
                    logger.warning(f"Found {invalid_dates} unparseable date values in column '{col}', converted to NaT.")

        logger.info("Data transformation completed successfully.")
        return df
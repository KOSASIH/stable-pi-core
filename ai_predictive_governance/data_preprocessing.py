import pandas as pd
from typing import Dict, Any, List

class DataPreprocessor:
    """
    A class to preprocess collected on-chain and off-chain data for AI-driven predictive governance.

    Attributes:
        data (Dict[str, Any]): The raw data collected from on-chain and off-chain sources.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def clean_data(self) -> pd.DataFrame:
        """
        Cleans the collected data by removing duplicates and handling missing values.

        Returns:
            pd.DataFrame: A cleaned DataFrame containing the processed data.
        """
        # Combine on-chain and off-chain data into a single DataFrame
        on_chain_df = pd.DataFrame(self.data.get("on_chain", []))
        off_chain_df = pd.DataFrame(self.data.get("off_chain", []))
        combined_df = pd.concat([on_chain_df, off_chain_df], ignore_index=True)

        # Remove duplicates
        combined_df.drop_duplicates(inplace=True)

        # Handle missing values (e.g., fill with forward fill method)
        combined_df.fillna(method='ffill', inplace=True)

        return combined_df

    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalizes numerical features in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to normalize.

        Returns:
            pd.DataFrame: A normalized DataFrame.
        """
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numerical_cols] = (df[numerical_cols] - df[numerical_cols].mean()) / df[numerical_cols].std()
        return df

    def preprocess(self) -> pd.DataFrame:
        """
        Preprocesses the collected data by cleaning and normalizing it.

        Returns:
            pd.DataFrame: A DataFrame containing the cleaned and normalized data.
        """
        cleaned_data = self.clean_data()
        normalized_data = self.normalize_data(cleaned_data)
        return normalized_data

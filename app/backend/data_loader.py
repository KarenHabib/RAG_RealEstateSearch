import pandas as pd
import logging

def load_data(filepath):
    try:
        # Load the dataset
        data = pd.read_csv(filepath)       
        return data

    except FileNotFoundError:
        logging.error("Data file not found.")
        raise
    except pd.errors.EmptyDataError:
        logging.error("Data file is empty.")
        raise
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise
    
properties_data = load_data("data/uae_real_estate_2024.csv")
from openai import AzureOpenAI 
import pandas as pd 
import logging
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path= "../../.env")

AEND = os.getenv("AZURE_ENDPOINT")
AKEY = os.getenv("API_KEY")
AV = os.getenv("API_VERSION")

# Azure OpenAI Setup 
client = AzureOpenAI( azure_endpoint=AEND, api_key=AKEY, api_version= AV) 

def generate_embeddings(text): 
    try:
        response = client.embeddings.create( model="gpt-4", input=text ) 
        return response['data'][0]['embedding'] 
    except Exception as e:
        logging.error(f"Error generating embedding for text '{text}': {e}")
        return None  

def index_properties(filepath): 
    try:
        data = pd.read_csv(filepath) 
        data['embedding'] = data['description'].apply(generate_embeddings) 
        return data 
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None
    except Exception as e:
        logging.error(f"Error indexing properties: {e}")
        return None

if __name__ == "__main__":
    try:
        properties_data = index_properties("data/uae_real_estate_2024.csv")
        if properties_data is not None:
            properties_data.to_csv("data/indexed_uae_real_estate_2024.csv", index=False)
        else:
            logging.error("Failed to index properties. Check previous error logs.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import logging

def load_properties(filepath):
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None
    except Exception as e:
        logging.error(f"Error loading properties: {e}")
        return None

properties_data = load_properties("data/uae_real_estate_2024.csv") 

if properties_data is not None:
    try:
        properties_data['furnishing'] = properties_data['furnishing'].fillna("").str.upper()
        properties_data['bedrooms'] = properties_data['bedrooms'].fillna("")  # Handle mixed types (e.g., "studio", "7+")
        properties_data['bathrooms'] = properties_data['bathrooms'].fillna("")
        properties_data['description'] = properties_data['description'].fillna("")
        properties_data['search_text'] = properties_data['title'].astype(str) + " " + properties_data['displayAddress'].astype(str) + " " + properties_data['description'].astype(str)
    except Exception as e:
        logging.error(f"Error preprocessing properties data: {e}")

def retrieve_properties(query): 
    try:
        # Vectorize the text 
        vectorizer = TfidfVectorizer()  # Initialize the vectorizer
        property_vectors = vectorizer.fit_transform(properties_data['search_text'])  # Calculate document-term matrix
        query_vector = vectorizer.transform([query])
        
        # Compute similarity 
        similarity = cosine_similarity(query_vector, property_vectors).flatten() 
        top_matches = similarity.argsort()[-5:][::-1] # Get top 5 matches 
        
        # Return top results 
        return properties_data.iloc[top_matches].to_dict(orient="records")
    except Exception as e:
        logging.error(f"Error retrieving properties: {e}")
        return []

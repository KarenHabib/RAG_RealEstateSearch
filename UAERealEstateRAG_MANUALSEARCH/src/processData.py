import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        # Filter out unverified listings
        data = data[data['verified'] == True]
        
        # Keep exact values as they are in CSV
        data['furnishing'] = data['furnishing'].fillna("").str.upper()
        data['bedrooms'] = data['bedrooms'].fillna("")  # Handle mixed types (e.g., "studio", "7+")
        data['bathrooms'] = data['bathrooms'].fillna("")  # Handle mixed types (e.g., "none", "7+")

        return data
    except FileNotFoundError:
        print("Error: The specified file was not found.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()

def build_index(data, column='description'):
    try:
        if data.empty:
            print("Warning: No data to index.")
            return None, None

        # Vectorize property descriptions
        vectorizer = TfidfVectorizer()
        data_vectors = vectorizer.fit_transform(data[column].fillna(''))
        return vectorizer, data_vectors
    except Exception as e:
        print(f"An error occurred while building the index: {e}")
        return None, None
# import pandas as pd 
# from sklearn.feature_extraction.text import TfidfVectorizer 

# def load_data(filepath): 
#     try: 
#         data = pd.read_csv(filepath) 
#         # Filter out non-residential listings and only "sell" priceDuration
#         data = data[ 
#             (data['type'] == "Residential for Sale") & 
#             (data['priceDuration'] == "sell") 
#         ] 
#         # Fill missing values and normalize values 
#         data['furnishing'] = data['furnishing'].fillna("UNKNOWN").str.upper() 
#         data['verified'] = data['verified'].fillna(False).astype(bool) 
#         return data 
#     except FileNotFoundError: 
#         print("Error: The specified file was not found.") 
#         return pd.DataFrame() # Return empty DataFrame as fallback 
#     except pd.errors.EmptyDataError: 
#         print("Error: The file is empty.") 
#         return pd.DataFrame() 
#     except Exception as e: 
#         print(f"An unexpected error occurred: {e}") 
#         return pd.DataFrame() 
    
# def build_index(data, column='description'): 
#     try: 
#         # Check if data is not empty 
#         if data.empty: 
#             print("Warning: No data to index.") 
#             return None, None 
#         # Vectorize property descriptions 
#         vectorizer = TfidfVectorizer() 
#         data_vectors = vectorizer.fit_transform(data[column].fillna('')) 
#         return vectorizer, data_vectors 
#     except Exception as e: 
#         print(f"An error occurred while building the index: {e}") 
#         return None, None



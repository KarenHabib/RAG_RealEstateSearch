import pandas as pd
from src.processData import load_data, build_index
from src.openai_integration import generate_response

class RealEstateChatbot:
    def __init__(self, data_path):

        self.data = load_data(data_path)
        # print(self.data.head())
        self.vectorizer, self.data_vectors = build_index(self.data)

        # self.data['bedrooms'] = pd.to_numeric(self.data['bedrooms'], errors='coerce').fillna(0).astype(int)
        # self.data['bathrooms'] = pd.to_numeric(self.data['bathrooms'], errors='coerce').fillna(0).astype(int)
        # self.data['price'] = pd.to_numeric(self.data['price'], errors='coerce').fillna(0)
        # self.data['sizeMin'] = pd.to_numeric(self.data['sizeMin'], errors='coerce').fillna(0)

    def search_properties(self, location, bedrooms=None, bathrooms=None, max_price=None, furnishing=None):
        try:
            # Filter only verified properties and those matching location
            filtered_data = self.data[
                (self.data['verified'] == True) & 
                (self.data['displayAddress'].str.contains(location, case=False, na=False))
            ]
            
            # Optional filters: apply only if values are provided
            # Apply filters only if values are provided
            if bedrooms is not None:
                # Handle "studio" case
                if str(bedrooms).lower() == "studio":
                    filtered_data = filtered_data[filtered_data['bedrooms'].str.lower() == "studio"]
                # Handle "7+" case for 7 or more bedrooms
                elif isinstance(bedrooms, int) and bedrooms >= 7:
                    filtered_data = filtered_data[filtered_data['bedrooms'] == "7+"]
                # Handle exact numeric match for bedroom count
                else:
                    # Convert bedroom column to numeric for exact matching
                    numeric_bedrooms = pd.to_numeric(filtered_data['bedrooms'], errors='coerce')
                    filtered_data = filtered_data[numeric_bedrooms == int(bedrooms)]
                
            if bathrooms is not None:
                # Handle "none" or 0 bathrooms case
                if str(bathrooms).lower() == "none" or bathrooms == 0:
                    filtered_data = filtered_data[filtered_data['bathrooms'].str.lower() == "none"]
                # Handle "7+" case for 7 or more bathrooms
                elif isinstance(bathrooms, int) and bathrooms >= 7:
                    filtered_data = filtered_data[filtered_data['bathrooms'] == "7+"]
                # Handle exact numeric match for bathroom count
                else:
                    # Convert bathroom column to numeric for exact matching
                    numeric_bathrooms = pd.to_numeric(filtered_data['bathrooms'], errors='coerce')
                    filtered_data = filtered_data[numeric_bathrooms == int(bathrooms)]
                
            if max_price is not None:
                # Filter for properties priced at or below the maximum price
                filtered_data = filtered_data[filtered_data['price'] <= max_price]
                
            if furnishing:
                # Normalize furnishing input to uppercase and filter
                furnishing = furnishing.upper()
                filtered_data = filtered_data[filtered_data['furnishing'] == furnishing]

            # Check if any properties match the criteria
            if filtered_data.empty:
                return None  # Return None if no properties match
            
            # Select only the necessary columns and rename them for display
            display_data = filtered_data[['title', 'displayAddress', 'bedrooms', 'sizeMin', 'price', 'description']]
            display_data.columns = ['Property', 'Address', 'Rooms', 'Area', 'Price', 'Description']
            return display_data

        except Exception as e:
            print(f"An error occurred during property search: {e}")
            return None

    # def get_response(self, location, bedrooms=None, bathrooms=None, max_price=None, furnishing=None):
    #     try:
    #         # Search for properties based on the criteria
    #         properties_summary = self.search_properties(
    #             location=location,
    #             bedrooms=bedrooms,
    #             bathrooms=bathrooms,
    #             max_price=max_price,
    #             furnishing=furnishing
    #         )

    #         # If no properties found, return that message directly
    #         if properties_summary is None:
    #             return "No properties found matching your criteria."

    #         # Generate a response based on the found properties
    #         # Convert the data to a text summary suitable for a language model
    #         properties_text = properties_summary[['Property', 'Address', 'Rooms', 'Area', 'Price']].to_string(index=False)
    #         prompt = f"Summarize the following properties: {properties_text}"
    #         response = generate_response(prompt)
    #         return response

    #     except Exception as e:
    #         print(f"An error occurred in generating response: {e}")
    #         return "Error generating a response. Please try again."
        
    # def generate_chatbot_response(self, query):
    #     try:
    #         # Formulate a prompt based on the query
    #         prompt = f"Retrieve and summarize UAE real estate properties based on this query: '{query}'"
    #         response = generate_response(prompt)
    #         return response
    #     except Exception as e:
    #         print(f"An error occurred in generating chatbot response: {e}")
    #         return "Error generating a response. Please try again."
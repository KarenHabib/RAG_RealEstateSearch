import os
from dotenv import load_dotenv
from openai import AzureOpenAI 
load_dotenv(dotenv_path= "../../.env")

AEND = os.getenv("AZURE_ENDPOINT")
AKEY = os.getenv("API_KEY")
AV = os.getenv("API_VERSION")

# Azure OpenAI Setup 
client = AzureOpenAI( azure_endpoint=AEND, api_key=AKEY, api_version= AV) 


def detect_conversation(query): 
    # Basic keywords for casual conversation 
    conversational_keywords = ["hello", "hi", "how are you", "what's up", "hey"] 
    return any(keyword in query.lower() for keyword in conversational_keywords) 

def format_properties(properties): 
    formatted_properties = "" 
    for prop in properties: 
        formatted_properties += ( f"Title: {prop['title']}\n" f"Location: {prop['displayAddress']}\n" f"Bedrooms: {prop['bedrooms']}\n" f"Bathrooms: {prop['bathrooms']}\n" f"Price: {prop['price']}\n" f"Description: {prop['description']}\n\n" ) 
    return formatted_properties 
    
def generate_response(query, properties=None): 
    if detect_conversation(query): 
        # Handle general conversation 
        response = client.chat.completions.create( model="gpt-4", messages=[ {"role": "system", "content": "You are a friendly assistant."}, {"role": "user", "content": query} ] ) 
        return response.choices[0].message.content 
    
    # If properties data is provided, generate a real estate response 
    if properties: 
        properties_text = format_properties(properties) 
        prompt = ( "You are an expert in UAE real estate. Given the following properties, provide the best match and a summary:\n\n" f"{properties_text}\n\n" "Respond to the user's query as a helpful assistant providing property recommendations." ) 
        response = client.chat.completions.create( model="gpt-4", messages=[ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt} ] ) 
        return response.choices[0].message.content # Fallback if no properties and not a conversation 
    
    return "I didn't find any properties that match your criteria. Could you provide more details?"

# from openai import AzureOpenAI 

# # Azure OpenAI Setup 

# def format_properties(properties): 
#     formatted_properties = "" 
#     for prop in properties: 
#         formatted_properties += ( f"Title: {prop['title']}\n" f"Location: {prop['displayAddress']}\n" f"Bedrooms: {prop['bedrooms']}\n" f"Bathrooms: {prop['bathrooms']}\n" f"Price: {prop['price']}\n" f"Description: {prop['description']}\n\n" ) 
#     return formatted_properties 

# def generate_response(properties): 
#     properties_text = format_properties(properties) 
#     prompt = ( "You are an expert in UAE real estate. Given the following properties, provide the best match and a summary:\n\n" f"{properties_text}\n\n" "Respond to the user's query as a helpful assistant providing property recommendations." ) 
#     response = client.chat.completions.create( model="gpt-4", messages=[ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt} ] ) 
#     return response.choices[0].message.content
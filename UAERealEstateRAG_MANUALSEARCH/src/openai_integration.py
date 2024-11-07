import openai 

openai.api_type = "azure" 
openai.api_base = "https://assessment.openai.azure.com/" 
openai.api_version = "2024-05-13" 
openai.api_key = "XXXXXXXXXX" 

# def generate_response(prompt):
#     try:
#         # Use OpenAI's completion API to generate a response
#         response = openai.Completion.create(
#             engine="gpt-4o",
#             prompt=prompt,
#             max_tokens=150
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         print(f"Error generating response: {e}")
#         return "Sorry, I couldn't process your request at the moment."
    


import streamlit as st
import re
from src.chatbot import RealEstateChatbot
from src.openai_integration import generate_response


# Function to detect and clean HTML tags if needed
def clean_html(description):
    # Remove HTML tags (if you want to strip them)
    clean_description = re.sub(r'<.*?>', '', description)
    return clean_description

# Initialize the chatbot with data path
chatbot = RealEstateChatbot(data_path="data/uae_real_estate_2024.csv")

st.title("UAE Real Estate RAG Chatbot")

# Choice between manual search and chatbot
option = st.radio("Choose your search method:", ("Manual Search", "Chatbot"))
if option == "Manual Search":
    # Required input for location
    location = st.text_input("Enter location:", placeholder="e.g., Dubai")
    if not location:
        st.warning("Please enter a location to proceed.")
    else:
        # Optional inputs
        bedrooms = st.number_input("Number of bedrooms (optional)", min_value=1, max_value=10, step=1, value=None)
        bathrooms = st.number_input("Number of bathrooms (optional)", min_value=1, max_value=10, step=1, value=None)
        max_price = st.number_input("Maximum price (optional)", min_value=1, value=None)
        furnishing = st.selectbox("Furnishing (optional)", ["", "YES", "NO", "PARTLY", "UNKNOWN"])

        # Trigger search when "Search" button is clicked
        if st.button("Search"):
            # Perform search and retrieve matching properties
            results = chatbot.search_properties(
                location=location,
                bedrooms=bedrooms if bedrooms else None,
                bathrooms=bathrooms if bathrooms else None,
                max_price=max_price if max_price else None,
                furnishing=furnishing if furnishing else None
            )

            if results is None:
                st.write("No properties found matching your criteria.")
            else:
                for _, row in results.iterrows():
                    st.write(f"**Property**: {row['Property']}")
                    st.write(f"**Address**: {row['Address']}")
                    st.write(f"**Rooms**: {row['Rooms']}")
                    st.write(f"**Area**: {row['Area']}")
                    # print(row['Price'])
                    st.write(f"**Price**: {row['Price']} AED")
                    
                    # Display Description, check if it's HTML or plain text
                    description = row['Description']
                    if '<' in description:  # If description contains HTML tags
                        try:
                            st.markdown(description, unsafe_allow_html=True)  # Render HTML content properly
                        except:
                            st.write(clean_html(description))  # Fallback to stripped text if rendering fails
                    else:
                        st.write(description)  # Display plain text description directly

                    st.write("---")  # Divider between properties
else:   
    print("Hello AI")
# Chatbot section
# elif option == "Chatbot":
    # query = st.text_input("Ask the chatbot:", placeholder="e.g., Find me a 3-bedroom villa in Abu Dhabi")
    
    # if st.button("Submit Query"):
    #     response = chatbot.generate_chatbot_response(query)
    #     st.write(response)
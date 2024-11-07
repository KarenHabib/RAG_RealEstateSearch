import streamlit as st 
from backend.retriever import retrieve_properties 
from backend.rag_generator import generate_response 

st.title("UAE Real Estate RAG Chatbot") 
# Initialize session state to store conversation history 
if "history" not in st.session_state: 
    st.session_state.history = [] 

# Chat input 
user_query = st.chat_input("Enter your property search query") 

# Process the user query 
if user_query: 
    
    # Retrieve relevant properties 
    results = retrieve_properties(user_query) 
    
    # Generate a response based on retrieved properties 
    response = generate_response(user_query, results) 
    
    # Store the conversation in session state 
    st.session_state.history.append({"role": "user", "content": user_query}) 
    st.session_state.history.append({"role": "assistant", "content": response}) 
    
# Display chat history 
for message in st.session_state.history: 
    if message["role"] == "user": 
        st.write(f"**User:** {message['content']}") 
    elif message["role"] == "assistant": 
        st.write(f"**Assistant:** {message['content']}")
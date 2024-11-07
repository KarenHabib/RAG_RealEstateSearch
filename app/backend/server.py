from fastapi import FastAPI
from backend.retriever import retrieve_properties
from backend.rag_generator import generate_response

app = FastAPI()

@app.get("/query")
def query_property_search(query: str):
    retrieved_data = retrieve_properties(query)
    response = generate_response(retrieved_data)
    return {"response": response}
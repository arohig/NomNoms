from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Create the FastAPI app instance
app = FastAPI()

# Define a simple root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI service!"}

# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# Import your router files
from routers import general, basket, products, users 

# Load environment variables from .env file
load_dotenv()

# --- API Security Setup ---
API_KEY = os.getenv("APP_API_KEY")
API_KEY_NAME = "MCP_API_KEY" # This is the header name clients will use

# This defines the security scheme. FastAPI uses this for the auto-generated docs.
api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header_auth)):
    """
    This is the dependency function that will be run on every request.
    It checks if the provided MCP_API_KEY header matches the one in our environment.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403, 
            detail="Could not validate credentials"
        )

# --- Create the main app instance with the global dependency ---
app = FastAPI(
    title="Main E-Commerce Service",
    description="Every route in this service is protected with an access token MCP_API_KEY",
    version="1.0.0",
    # This line applies the verify_api_key function to EVERY route in the app
    dependencies=[Depends(verify_api_key)]
)

# --- Include each router ---
# Because the dependency is global, all routes in these routers are now protected.
app.include_router(general.router)
app.include_router(basket.router)
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MCP Server"}

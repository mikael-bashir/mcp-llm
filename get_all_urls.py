import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "/"))
if project_root not in sys.path:
    sys.path.append(project_root)

from fastapi import FastAPI
from pydantic import BaseModel
from lib.helpers.server import get_urls

app = FastAPI()

class RequestBody(BaseModel):
    query: str

@app.get("/api/mcp/v1/get_all_urls")
def get_all_urls(body: RequestBody):
    context = get_urls()
    return context

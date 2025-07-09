import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "/"))
if project_root not in sys.path:
    sys.path.append(project_root)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from lib.helpers.server import get_urls
from jsonref import JsonRef
import yaml

app = FastAPI()

class RequestBody(BaseModel):
    query: str

@app.get("/api/mcp/v1/get_all_urls")
def get_all_urls():
    context = get_urls()
    return context

# --- Load and RESOLVE the spec once on startup ---
resolved_swagger_spec = None
try:
    openapi_path = "openapi.yaml"
    with open(openapi_path, 'r') as f:
        # Load the raw YAML file
        raw_swagger_spec = yaml.safe_load(f)
        # Resolve all references immediately to create a complete spec object
        if raw_swagger_spec:
            resolved_swagger_spec = JsonRef.replace_refs(raw_swagger_spec)
except FileNotFoundError:
    print(f"ERROR: Could not find openapi.yaml at the expected path: {openapi_path}")


class RequestBody(BaseModel):
    url_path: str

@app.post("/api/mcp/v1/get_url_swagger")
def get_swagger_for_url(body: RequestBody):
    if resolved_swagger_spec is None:
        raise HTTPException(status_code=500, detail="OpenAPI spec file not found or failed to load.")

    target_path = body.url_path
    paths_in_spec = resolved_swagger_spec.get("paths", {})
    specification = paths_in_spec.get(target_path)

    if specification:

        return {
            "path": target_path,
            "specification": specification
        }
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No specification found for URL path: {target_path}"
        )

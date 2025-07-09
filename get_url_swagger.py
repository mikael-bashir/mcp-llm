import sys
import os
import yaml
from pathlib import Path  # Make sure pathlib is imported
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jsonref import JsonRef

# --- Path setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root_str = os.path.abspath(os.path.join(current_dir, "/"))
if project_root_str not in sys.path:
    sys.path.append(project_root_str)

# Convert the string path to a Path object
project_root = Path(project_root_str)
# --- End of path setup ---

app = FastAPI()

# --- Load and RESOLVE the spec once on startup ---
resolved_swagger_spec = None
try:
    openapi_path = project_root / "public" / "openapi.yaml"
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

@app.get("/api/mcp/v1/get_url_swagger")
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

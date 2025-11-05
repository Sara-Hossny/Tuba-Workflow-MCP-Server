from fastmcp import FastMCP
import requests
from dotenv import load_dotenv
import os
import json
from typing import Dict, Any, List, Union, Optional
import base64
import sys
from pydantic import Json

load_dotenv()

TUBA_WORKFLOW_API_URL = "https://tuba.ai/workflow_builder_api"
ACCESS_TOKEN = os.environ.get("TUBA_WORKFLOW_ACCESS_TOKEN")

# Initialize FastMCP
mcp = FastMCP(name="TubaWorkflow")


def log_to_stderr(*args, **kwargs):
    """Prints to stderr to avoid interfering with stdio transport."""
    print(*args, file=sys.stderr, **kwargs)


@mcp.tool(description="Run the workflow for a given project")
def run() -> str:
    """Run the workflow, requiring authentication"""
    if not ACCESS_TOKEN:
        return {"error": "Authentication required"}

    try:
        resp = requests.post(
            f"{TUBA_WORKFLOW_API_URL}/run",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}


@mcp.tool(description="Get the current workflow status")
def status() -> str:
    """Get workflow status, requiring authentication"""
    if not ACCESS_TOKEN:
        return {"error": "Authentication required"}

    try:
        resp = requests.get(
            f"{TUBA_WORKFLOW_API_URL}/status",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}


@mcp.tool(description="Fetch workflow results")
def result() -> dict:
    """Fetch workflow results, requiring authentication"""
    if not ACCESS_TOKEN:
        return {"error": "Authentication required"}

    resp = requests.get(
        f"{TUBA_WORKFLOW_API_URL}/result",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    # check if the response is a file
    if resp.headers.get("Content-Type") == "application/zip":
        # save the file to the local directory
        with open("result.zip", "wb") as f:
            f.write(resp.content)
        return {
            "status": "success",
            "message": "result.zip has been saved to the current directory.",
        }
    else:
        return resp.json()


@mcp.tool(description="Get workflow blocks configuration")
def get_workflow_blocks() -> dict:
    """Fetch the current workflow blocks for the authenticated project"""
    if not ACCESS_TOKEN:
        return {"error": "Authentication required"}

    resp = requests.get(
        f"{TUBA_WORKFLOW_API_URL}/get-workflow-blocks",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    return resp.json()


def _process_local_files(files, files_payload, opened_file_handles):
    if files:
        for field_name, path_or_paths in files.items():
            if isinstance(path_or_paths, list):
                for file_path in path_or_paths:
                    f = open(file_path, "rb")
                    opened_file_handles.append(f)
                    files_payload.append((field_name, (os.path.basename(file_path), f)))
            else:
                file_path = path_or_paths
                f = open(file_path, "rb")
                opened_file_handles.append(f)
                files_payload.append((field_name, (os.path.basename(file_path), f)))


def _process_remote_urls(file_urls, files_payload):
    if file_urls:
        for field_name, url_or_urls in file_urls.items():
            if isinstance(url_or_urls, list):
                urls_iter = url_or_urls
            else:
                urls_iter = [url_or_urls]
            for u in urls_iter:
                r = requests.get(u, stream=True)
                r.raise_for_status()
                filename_guess = u.split("/")[-1] or "file"
                files_payload.append((field_name, (filename_guess, r.content)))


def _process_base64_blobs(file_blobs, files_payload):
    if file_blobs:

        def add_blob(field: str, blob: Dict[str, Any]):
            filename = blob.get("filename") or "file"
            content_b64 = blob.get("content_base64") or ""
            content_type = blob.get("content_type") or None
            try:
                content_bytes = base64.b64decode(content_b64)
            except Exception:
                content_bytes = b""
            if content_type:
                files_payload.append((field, (filename, content_bytes, content_type)))
            else:
                files_payload.append((field, (filename, content_bytes)))

        for field_name, blob_or_blobs in file_blobs.items():
            if isinstance(blob_or_blobs, list):
                for b in blob_or_blobs:
                    add_blob(field_name, b)
            else:
                add_blob(field_name, blob_or_blobs)


@mcp.tool(
    description="Update workflow blocks data. The workflow_blocks parameter is a JSON object that contains the workflow block data in this format: {<block_id>: {<param_name>: <value>}}. The files parameter is a mapping of the file field name to the file path. The file field name should be in the format <block_id>_<param_name>:file_path/file_url/file_blob."
)
def update_workflow_blocks_data(
    workflow_blocks: Optional[Json] = None,
    files: Optional[Json] = None,
    file_urls: Optional[Json] = None,
    file_blobs: Optional[Json] = None,
) -> dict:
    if not ACCESS_TOKEN:
        return {"error": "Authentication required"}

    form_data = {"workflow_blocks": json.dumps(workflow_blocks or {})}
    files_payload: List = []
    opened_file_handles: List = []

    try:
        _process_local_files(files, files_payload, opened_file_handles)
        _process_remote_urls(file_urls, files_payload)
        _process_base64_blobs(file_blobs, files_payload)

        resp = requests.patch(
            f"{TUBA_WORKFLOW_API_URL}/update-workflow-blocks-data",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            data=form_data,
            files=files_payload if files_payload else None,
        )

        try:
            return resp.json()
        except Exception:
            return {"status_code": resp.status_code, "text": resp.text}
    finally:
        for f in opened_file_handles:
            try:
                f.close()
            except Exception:
                pass


if __name__ == "__main__":
    mcp.run()

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import time
from typing import Any, Dict

import google.auth
import httpx
from fastapi import FastAPI, HTTPException
from google.adk.cli.fast_api import get_fast_api_app
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export
from vertexai import agent_engines

from financial_advisor.utils.gcs import create_bucket_if_not_exists
from financial_advisor.utils.tracing import CloudTraceLoggingSpanExporter
from financial_advisor.utils.typing import Feedback
from financial_advisor.response_extractor import (
    extract_financial_coordinator_output,
    extract_all_agent_outputs,
    extract_conversation_summary,
)

_, project_id = google.auth.default()
allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

bucket_name = f"gs://{project_id}-my-fullstack-agent-logs-data"
create_bucket_if_not_exists(
    bucket_name=bucket_name, project=project_id, location="us-central1"
)

provider = TracerProvider()
processor = export.BatchSpanProcessor(CloudTraceLoggingSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Agent Engine session configuration
# Use environment variable for agent name, default to project name
agent_name = os.environ.get("AGENT_ENGINE_SESSION_NAME", "my-fullstack-agent")

# Check if an agent with this name already exists
existing_agents = list(agent_engines.list(filter=f"display_name={agent_name}"))

if existing_agents:
    # Use the existing agent
    agent_engine = existing_agents[0]
else:
    # Create a new agent if none exists
    agent_engine = agent_engines.create(display_name=agent_name)

session_service_uri = f"agentengine://{agent_engine.resource_name}"

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=bucket_name,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
)
app.title = "my-fullstack-agent"
app.description = "API for interacting with the Agent my-fullstack-agent"


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    return {"status": "success"}


@app.post("/extract_financial_output")
async def extract_financial_output(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract financial coordinator output from agent response.

    This endpoint takes the same request as /run but extracts and returns
    only the final financial coordinator output in a clean format.

    Args:
        request_data: The request data to send to the /run endpoint

    Returns:
        Dictionary containing the extracted financial coordinator output
    """
    start_time = time.time()

    try:
        # Make request to the /run endpoint
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                "http://localhost:8000/run",
                json=request_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Run endpoint failed: {response.text}",
                )

            response_data = response.json()

        # Extract the financial coordinator output
        financial_output = extract_financial_coordinator_output(response_data)

        processing_time = time.time() - start_time

        if financial_output:
            result = {
                "financial_coordinator_output": financial_output,
                "metadata": {
                    "endpoint_used": "/extract_financial_output",
                    "processing_time_seconds": processing_time,
                    "extraction_successful": True,
                    "timestamp": time.time(),
                },
            }
            return result
        else:
            result = {
                "financial_coordinator_output": None,
                "metadata": {
                    "endpoint_used": "/extract_financial_output",
                    "processing_time_seconds": processing_time,
                    "extraction_successful": False,
                    "error": "No financial_coordinator_output found",
                    "timestamp": time.time(),
                },
            }
            return result

    except httpx.TimeoutException:
        processing_time = time.time() - start_time
        raise HTTPException(status_code=408, detail="Request timed out")
    except Exception as e:
        processing_time = time.time() - start_time
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/run_with_extraction")
async def run_with_extraction(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced run endpoint that returns both raw response and extracted financial output.

    This endpoint provides the best of both worlds - you get the full raw response
    AND the clean extracted financial coordinator output.

    Args:
        request_data: The request data for the agent

    Returns:
        Dictionary containing both raw response and extracted output
    """
    start_time = time.time()

    try:
        # Get the base URL dynamically
        base_url = os.getenv("BASE_URL", "http://localhost:8000")

        # Make request to the /run endpoint
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{base_url}/run",
                json=request_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Run endpoint failed: {response.text}",
                )

            response_data = response.json()

        # Extract the financial coordinator output
        financial_output = extract_financial_coordinator_output(response_data)
        all_outputs = extract_all_agent_outputs(response_data)
        conversation_summary = extract_conversation_summary(response_data)

        processing_time = time.time() - start_time

        result = {
            "raw_response": response_data,
            "extracted_outputs": {
                "financial_coordinator_output": financial_output,
                "all_agent_outputs": all_outputs,
                "conversation_summary": conversation_summary,
            },
            "metadata": {
                "endpoint_used": "/run_with_extraction",
                "processing_time_seconds": processing_time,
                "extraction_successful": financial_output is not None,
                "timestamp": time.time(),
                "total_response_entries": len(response_data),
            },
        }

        return result

    except httpx.TimeoutException:
        processing_time = time.time() - start_time
        raise HTTPException(status_code=408, detail="Request timed out")
    except Exception as e:
        processing_time = time.time() - start_time
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/extract_all_outputs")
async def extract_all_outputs(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract outputs from all agents in the response.

    Args:
        request_data: The request data to send to the /run endpoint

    Returns:
        Dictionary containing outputs from all agents
    """
    start_time = time.time()

    try:
        # Get the base URL dynamically
        base_url = os.getenv("BASE_URL", "http://localhost:8000")

        # Make request to the /run endpoint
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{base_url}/run",
                json=request_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Run endpoint failed: {response.text}",
                )

            response_data = response.json()

        # Extract all agent outputs
        all_outputs = extract_all_agent_outputs(response_data)
        conversation_summary = extract_conversation_summary(response_data)

        processing_time = time.time() - start_time

        result = {
            "agent_outputs": all_outputs,
            "conversation_summary": conversation_summary,
            "metadata": {
                "endpoint_used": "/extract_all_outputs",
                "processing_time_seconds": processing_time,
                "extraction_successful": True,
                "timestamp": time.time(),
            },
        }
        return result

    except httpx.TimeoutException:
        processing_time = time.time() - start_time
        raise HTTPException(status_code=408, detail="Request timed out")
    except Exception as e:
        processing_time = time.time() - start_time
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
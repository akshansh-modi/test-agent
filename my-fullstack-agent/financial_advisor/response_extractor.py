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

import json
import re
from typing import Any, Dict, Optional


def extract_financial_coordinator_output(response_data: list) -> Optional[Dict[str, Any]]:
    """
    Extract financial_coordinator_output from the response data.
    
    The financial coordinator output is typically found in the last entry
    with author="financial_coordinator" in the actions.stateDelta field.
    
    Args:
        response_data: List of response entries from the agent
        
    Returns:
        Parsed JSON dict of the financial coordinator output, or None if not found
    """
    try:
        # Look for entries with author="financial_coordinator" that have stateDelta
        for i, entry in enumerate(reversed(response_data)):
            try:
                if (
                    entry.get("author") == "financial_coordinator" and 
                    "actions" in entry and 
                    "stateDelta" in entry["actions"] and
                    "financial_coordinator_output" in entry["actions"]["stateDelta"]
                ):
                    raw_output = entry["actions"]["stateDelta"]["financial_coordinator_output"]
                    
                    # Extract JSON from the string (remove ```json and ``` markers)
                    json_match = re.search(r'```json\s*\n(.*)\n```', raw_output, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1).strip()
                        parsed_output = json.loads(json_str)
                        return parsed_output
                        
            except Exception as e:
                continue
                
        return None
        
    except Exception as e:
        return None


def extract_all_agent_outputs(response_data: list) -> Dict[str, Any]:
    """
    Extract outputs from all agents in the response.
    
    Args:
        response_data: List of response entries from the agent
        
    Returns:
        Dictionary containing outputs from different agents
    """
    try:
        outputs = {
            "data_analyst_output": None,
            "trading_analyst_output": None,
            "risk_analyst_output": None,
            "execution_analyst_output": None,
            "financial_coordinator_output": None
        }
        
        for entry in response_data:
            try:
                if "actions" in entry and "stateDelta" in entry["actions"]:
                    state_delta = entry["actions"]["stateDelta"]
                    
                    # Check for different agent outputs
                    for key in outputs.keys():
                        if key in state_delta and outputs[key] is None:
                            raw_output = state_delta[key]
                            
                            # Try to parse JSON if it's a string with markers
                            if isinstance(raw_output, str):
                                json_match = re.search(r'```json\s*\n(.*)\n```', raw_output, re.DOTALL)
                                if json_match:
                                    json_str = json_match.group(1).strip()
                                    try:
                                        outputs[key] = json.loads(json_str)
                                    except json.JSONDecodeError:
                                        outputs[key] = raw_output
                                else:
                                    outputs[key] = raw_output
                            else:
                                outputs[key] = raw_output
                                
            except Exception as e:
                continue
                
        return outputs
        
    except Exception as e:
        return {}


def extract_conversation_summary(response_data: list) -> Dict[str, Any]:
    """
    Create a summary of the conversation flow.
    
    Args:
        response_data: List of response entries from the agent
        
    Returns:
        Dictionary containing conversation summary
    """
    try:
        summary = {
            "total_entries": len(response_data),
            "authors": [],
            "agent_calls": [],
            "final_output_found": False
        }
        
        for i, entry in enumerate(response_data):
            try:
                author = entry.get("author", "unknown")
                summary["authors"].append(author)
                
                # Check for function calls
                if "content" in entry and "parts" in entry["content"]:
                    for part in entry["content"]["parts"]:
                        if "functionCall" in part:
                            function_name = part["functionCall"].get("name", "unknown")
                            summary["agent_calls"].append({
                                "entry_index": i,
                                "function_name": function_name,
                                "author": author
                            })
                
                # Check if this entry has the final output
                if (
                    author == "financial_coordinator" and 
                    "actions" in entry and 
                    "stateDelta" in entry["actions"] and
                    "financial_coordinator_output" in entry["actions"]["stateDelta"]
                ):
                    summary["final_output_found"] = True
                    
            except Exception as e:
                continue
                
        return summary
        
    except Exception as e:
        return {}

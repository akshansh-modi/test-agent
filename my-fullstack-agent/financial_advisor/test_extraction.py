#!/usr/bin/env python3

import json
import sys
import os

def extract_financial_coordinator_output_simple(response_data: list):
    """Simple version of extraction function for testing."""
    import re
    
    try:
        print(f"Starting extraction from {len(response_data)} response entries")
        
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
                    print(f"Found financial_coordinator_output in entry {len(response_data) - i - 1}")
                    
                    # Extract JSON from the string (remove ```json and ``` markers)
                    json_match = re.search(r'```json\s*\n(.*)\n```', raw_output, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1).strip()
                        parsed_output = json.loads(json_str)
                        print("Successfully parsed financial coordinator output")
                        return parsed_output
                    else:
                        print("Could not find JSON markers in financial_coordinator_output")
                        print(f"Raw output preview: {raw_output[:200]}...")
                        
            except Exception as e:
                print(f"Error processing entry {i}: {str(e)}")
                continue
                
        print("No financial_coordinator_output found in response data")
        return None
        
    except Exception as e:
        print(f"Error extracting financial coordinator output: {str(e)}")
        return None

def test_extraction():
    """Test the extraction function with sample data from the file."""
    
    # Read the sample response file
    sample_file = "/Users/apple/development/test-agent/my-fullstack-agent/financial_advisor/sample_prompt_of_run.txt"
    
    try:
        with open(sample_file, 'r') as f:
            content = f.read()
            
        # Parse the JSON
        response_data = json.loads(content)
        
        print(f"Loaded response data with {len(response_data)} entries")
        
        # Test extraction
        result = extract_financial_coordinator_output_simple(response_data)
        
        if result:
            print("✅ Extraction successful!")
            print("📊 Financial Coordinator Output:")
            
            # Check key fields
            if "results_overall_score" in result:
                print(f"📈 Overall Score: {result['results_overall_score'].get('overall_score', 'N/A')}")
                
            if "session_metadata" in result:
                ticker = result['session_metadata'].get('market_ticker', 'N/A')
                print(f"🎯 Ticker: {ticker}")
                
            print(f"📋 Keys in result: {list(result.keys())}")
                
        else:
            print("❌ Extraction failed - no financial coordinator output found")
            
            # Debug: Check what we have
            print("\n🔍 Debug info:")
            for i, entry in enumerate(response_data):
                author = entry.get('author', 'unknown')
                has_actions = 'actions' in entry
                has_state_delta = has_actions and 'stateDelta' in entry['actions']
                has_fin_output = has_state_delta and 'financial_coordinator_output' in entry['actions']['stateDelta']
                
                print(f"Entry {i}: author='{author}', actions={has_actions}, stateDelta={has_state_delta}, fin_output={has_fin_output}")
        
    except FileNotFoundError:
        print(f"❌ Sample file not found: {sample_file}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_extraction()
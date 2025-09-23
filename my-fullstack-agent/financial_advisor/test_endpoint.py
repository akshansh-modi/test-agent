#!/usr/bin/env python3

import requests
import json

def test_extraction_endpoint():
    """Test the new /extract_financial_output endpoint."""
    
    # Test request data (using the format you provided earlier)
    request_data = {
        "app_name": "financial_advisor",
        "user_id": "test_user",
        "session_id": "test_session_123",
        "new_message": {
            "role": "user", 
            "parts": [{"text": "analyze ZOMATO stock"}]
        },
        "streaming": False
    }
    
    print("🚀 Testing /extract_financial_output endpoint...")
    print(f"📋 Request data: {json.dumps(request_data, indent=2)}")
    
    try:
        # Make request to our new endpoint
        response = requests.post(
            "http://localhost:8001/extract_financial_output",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minutes timeout
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            
            if result.get("financial_coordinator_output"):
                output = result["financial_coordinator_output"]
                print("📈 Financial Output Found:")
                
                if "results_overall_score" in output:
                    score_data = output["results_overall_score"]
                    print(f"🎯 Overall Score: {score_data.get('overall_score', 'N/A')}")
                    print(f"📝 Summary: {score_data.get('overall_summary', 'N/A')[:100]}...")
                    
                if "session_metadata" in output:
                    metadata = output["session_metadata"]
                    print(f"🏷️ Ticker: {metadata.get('market_ticker', 'N/A')}")
                    print(f"⚖️ Risk Attitude: {metadata.get('user_risk_attitude', 'N/A')}")
                    
                print(f"⏱️ Processing Time: {result['metadata'].get('processing_time_seconds', 'N/A'):.2f}s")
                
            else:
                print("❌ No financial coordinator output found")
                print(f"🔍 Error: {result['metadata'].get('error', 'Unknown')}")
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - the analysis is taking longer than expected")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error - make sure the server is running on port 8001")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_extraction_endpoint()
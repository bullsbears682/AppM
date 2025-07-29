#!/usr/bin/env python3
"""
Test script to debug ROI calculation issues
"""

import requests
import json

def test_calculation():
    """Test the ROI calculation API"""
    
    # Test data that should work
    test_data = {
        "company_name": "Test Company",
        "company_size": "medium",
        "current_industry": "saas",
        "project_type": "product_development",
        "target_industry": "saas",
        "currency": "USD",
        "custom_investment": 100000,
        "custom_timeline": 12
    }
    
    print("🧪 Testing ROI Calculation API")
    print("=" * 50)
    print(f"📤 Request Data: {json.dumps(test_data, indent=2)}")
    print()
    
    try:
        # Test the projects endpoint first
        print("🔍 Testing /api/projects endpoint...")
        projects_response = requests.get('http://localhost:5000/api/projects', timeout=10)
        print(f"Projects Status: {projects_response.status_code}")
        
        if projects_response.status_code == 200:
            projects_data = projects_response.json()
            print(f"Projects loaded: {len(projects_data.get('projects', []))}")
            if projects_data.get('projects'):
                # Use the first project type
                test_data['project_type'] = projects_data['projects'][0]['id']
                print(f"Using project type: {test_data['project_type']}")
        else:
            print(f"❌ Projects endpoint failed: {projects_response.text}")
        
        print()
        
        # Test the calculation endpoint
        print("🧮 Testing /api/calculate endpoint...")
        response = requests.post(
            'http://localhost:5000/api/calculate',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Calculation successful!")
            print(f"📥 Response: {json.dumps(result, indent=2)}")
        else:
            print("❌ Calculation failed!")
            print(f"Error Response: {response.text}")
            
            # Try to parse as JSON for better error info
            try:
                error_data = response.json()
                print(f"Error Details: {json.dumps(error_data, indent=2)}")
            except:
                pass
                
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running on localhost:5000")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Server may be overloaded.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    test_calculation()
#!/usr/bin/env python3
"""
Example: FastAPI Client Interaction

This script demonstrates how to interact with the FastAPI endpoints
for testing, integration, and remote usage scenarios.
"""

import json
import os
import requests
import time
from typing import Dict, Any

# Configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "8000")
BASE_URL = f"http://{API_HOST}:{API_PORT}"

def test_health_check() -> bool:
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Health check: {data['message']}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_ask_endpoint(prompt: str, model: str = "llama3.2:1b") -> Dict[str, Any]:
    """Test the /ask endpoint with a prompt."""
    try:
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        print(f"📤 Sending prompt: {prompt}")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/ask",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        duration = time.time() - start_time
        data = response.json()
        
        print(f"📥 Response ({duration:.2f}s): {data['response']}")
        return data
        
    except Exception as e:
        print(f"❌ Ask endpoint failed: {e}")
        return {}

def test_generate_endpoint(prompt: str, model: str = "llama3.2:1b") -> Dict[str, Any]:
    """Test the /generate endpoint (legacy compatibility)."""
    try:
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        response = requests.post(
            f"{BASE_URL}/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        data = response.json()
        print(f"📥 Generate response: {data['response']}")
        return data
        
    except Exception as e:
        print(f"❌ Generate endpoint failed: {e}")
        return {}

def main():
    """Run API client examples."""
    print("🚀 FastAPI Client Examples")
    print("=" * 40)
    
    # Test health check
    print("\n🏥 Testing Health Check")
    print("-" * 25)
    if not test_health_check():
        print("❌ API is not available. Make sure the container is running.")
        return
    
    # Test /ask endpoint
    print("\n💬 Testing /ask Endpoint")
    print("-" * 25)
    test_ask_endpoint("What is the capital of France?")
    
    # Test /generate endpoint (legacy)
    print("\n🔄 Testing /generate Endpoint (Legacy)")
    print("-" * 35)
    test_generate_endpoint("Explain machine learning in simple terms.")
    
    # Test with different model
    print("\n🎯 Testing with Different Model")
    print("-" * 30)
    test_ask_endpoint("Write a short poem about containers.", "llama3.2:1b")
    
    # Performance test
    print("\n⚡ Performance Test")
    print("-" * 18)
    prompts = [
        "Hello!",
        "What is 2+2?",
        "Name three colors.",
    ]
    
    total_time = 0
    for i, prompt in enumerate(prompts, 1):
        print(f"Test {i}/3:")
        start = time.time()
        test_ask_endpoint(prompt)
        duration = time.time() - start
        total_time += duration
        print(f"Duration: {duration:.2f}s\n")
    
    print(f"📊 Average response time: {total_time/len(prompts):.2f}s")
    
    print("\n✅ API client examples completed!")

if __name__ == "__main__":
    main()

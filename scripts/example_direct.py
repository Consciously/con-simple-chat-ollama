#!/usr/bin/env python3
"""
Example: Direct Ollama Interaction

This script demonstrates how to interact directly with Ollama within the container
for local LLM experiments, bypassing the FastAPI layer for maximum flexibility.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

import ollama
from loguru import logger

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.2:1b")

def main():
    """Example of direct Ollama interaction for experiments."""
    
    # Initialize Ollama client
    client = ollama.Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")
    
    print("🦙 Ollama Direct Interaction Example")
    print("=" * 40)
    
    try:
        # List available models
        models = client.list()
        print(f"📋 Available models: {len(models['models'])}")
        for model in models['models']:
            print(f"  - {model['name']} ({model['size']} bytes)")
        print()
        
        # Example 1: Simple generation
        print("🔥 Example 1: Simple Generation")
        print("-" * 30)
        prompt = "Explain what a container is in one sentence."
        print(f"Prompt: {prompt}")
        
        response = client.generate(
            model=DEFAULT_MODEL,
            prompt=prompt,
            stream=False
        )
        print(f"Response: {response['response']}")
        print()
        
        # Example 2: Streaming response
        print("🌊 Example 2: Streaming Response")
        print("-" * 30)
        prompt = "Write a haiku about programming."
        print(f"Prompt: {prompt}")
        print("Response: ", end="", flush=True)
        
        stream = client.generate(
            model=DEFAULT_MODEL,
            prompt=prompt,
            stream=True
        )
        
        for chunk in stream:
            print(chunk['response'], end="", flush=True)
        print("\n")
        
        # Example 3: Chat conversation
        print("💬 Example 3: Chat Conversation")
        print("-" * 30)
        
        messages = [
            {"role": "user", "content": "What is Docker?"},
            {"role": "assistant", "content": "Docker is a containerization platform."},
            {"role": "user", "content": "How does it differ from virtual machines?"}
        ]
        
        response = client.chat(
            model=DEFAULT_MODEL,
            messages=messages,
            stream=False
        )
        
        print("Chat response:")
        print(response['message']['content'])
        print()
        
        # Example 4: Model information
        print("ℹ️  Example 4: Model Information")
        print("-" * 30)
        
        model_info = client.show(DEFAULT_MODEL)
        print(f"Model: {model_info['details']['family']}")
        print(f"Parameters: {model_info['details'].get('parameter_size', 'Unknown')}")
        print(f"Quantization: {model_info['details'].get('quantization_level', 'Unknown')}")
        
    except Exception as e:
        logger.error(f"Error during Ollama interaction: {e}")
        sys.exit(1)
    
    print("\n✅ Direct interaction examples completed!")

if __name__ == "__main__":
    main()

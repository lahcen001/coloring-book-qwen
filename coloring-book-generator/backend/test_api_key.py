import os
import requests

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('DASHSCOPE_API_KEY')
BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation"

def test_api_key():
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen-max",
            "prompt": "test prompt",
            "size": "256x256",  # Using smaller size for testing
            "response_format": "url"
        }
        
        response = requests.post(BASE_URL, headers=headers, json=payload)
        
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        
        if response.status_code == 401:
            print("API Key is invalid or lacks proper permissions.")
        elif response.status_code == 200:
            print("API Key is valid and working.")
        else:
            print(f"Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"Error during API key test: {str(e)}")

if __name__ == "__main__":
    test_api_key()

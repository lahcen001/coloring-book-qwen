from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation"
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Configure CORS to allow requests from specific origins in production
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["POST", "OPTIONS"], allow_headers=["Content-Type"])

# Initialize DashScope client with the API key from environment variables
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('DASHSCOPE_API_KEY')
logging.info(f"API Key Loaded: {'*' * (len(api_key)-4) + api_key[-4:] if api_key else 'NOT FOUND'}")
if not api_key:
    logging.error("DASHSCOPE_API_KEY environment variable is not set.")
    exit(1)

# Additional validation
if len(api_key) < 32:
    logging.error("Invalid API Key length")
    exit(1)

# Removed explicit save_api_key usage

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'error': 'No prompt provided.'}), 400
    
    try:
        # Use DashScope API to generate a coloring image based on the prompt
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
"model": "qwen-max",
"prompt": prompt,
"size": "512x512",
"response_format": "url"
        }
        response = requests.post(
            DASHSCOPE_BASE_URL,
            headers=headers,
            json=payload
        )
        
        # Check response status and extract image URL
        try:
            response_data = response.json()
            
            if response.status_code == 200:
                image_url = response_data.get('url')
                return jsonify({'image_url': image_url})
            else:
                logging.error("Image generation failed: %s", response_data.get('message', 'Unknown error'))
                return jsonify({'error': response_data.get('message', 'Unknown error')}), response.status_code
        
        except ValueError:
            logging.error(f"Invalid response format - Status Code: {response.status_code}")
            logging.error(f"Response Headers: {response.headers}")
            logging.error(f"Raw Response Content: {response.text}")
            logging.error(f"Request URL: {response.request.url}")
            logging.error(f"Request Headers: {response.request.headers}")
            logging.error(f"Request Body: {response.request.body}")
            return jsonify({
                'error': 'Invalid response from server',
                'details': {
                    'status_code': response.status_code,
                    'content': response.text
                }
            }), 500
        
    except Exception as e:
        logging.exception("Unexpected server error")
        return jsonify({'error': 'Internal server error'}), 500
        logging.error("Unexpected error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500
        logging.error("Unexpected error: %s", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import time
    time.sleep(1)  # Brief delay to ensure clean start
    app.run(host='0.0.0.0', port=5013)

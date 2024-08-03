import os
import requests
import logging
import time

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def get_llm_response(user_input):
    url = "https://api.openai.com/v1/engines/davinci-002/completions"
    api_key = os.getenv('OPENAI_API_KEY')  # Get the API key from environment variable
    if not api_key:
        raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "prompt": user_input,
        "max_tokens": 150
    }

    max_retries = 5
    retry_delay = 1  # Initial delay of 1 second

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get('choices')[0].get('text').strip()
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:  # Too Many Requests
                logging.warning(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)  # Exponential backoff with a cap of 60 seconds
            else:
                logging.error(f"Error fetching response from LLM: {e}")
                return f"Error fetching response from LLM: {e}"
    return "Error: Max retries exceeded. Please try again later."

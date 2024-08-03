import os
import requests

def list_engines():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    response = requests.get('https://api.openai.com/v1/engines', headers=headers)
    response.raise_for_status()
    engines = response.json().get('data')
    
    for engine in engines:
        print(engine['id'])

if __name__ == '__main__':
    list_engines()

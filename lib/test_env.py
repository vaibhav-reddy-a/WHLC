import os

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"API Key: {api_key}")
else:
    print("API key not found. Set the OPENAI_API_KEY environment variable.")

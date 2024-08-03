from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from translate import translate_response
from llm_integration import get_llm_response

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    user_input = data.get('question')
    
    # Get knowledge base response
    kb_response = get_knowledge_base_response(user_input)
    
    # Get LLM response
    llm_response = get_llm_response(user_input)
    
    # Combine responses
    combined_response = combine_responses(kb_response, llm_response)
    
    # Translate response
    translated_response = translate_response(combined_response, 'hi')
    
    return jsonify({
        'response_en': combined_response,
        'response_hi': translated_response
    })

def get_knowledge_base_response(user_input):
    try:
        response = requests.post('http://127.0.0.1:5001/question', json={'question': user_input})
        response.raise_for_status()
        return response.json().get('response')
    except requests.exceptions.RequestException as e:
        return f"Error fetching knowledge base response: {e}"

def combine_responses(kb_response, llm_response):
    return f"{kb_response} {llm_response}"

if __name__ == '__main__':
    app.run(debug=True)

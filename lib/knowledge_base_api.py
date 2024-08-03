from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.tokenize import word_tokenize
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Download the punkt tokenizer
nltk.download('punkt')

app = Flask(__name__)
CORS(app)

knowledge_base = [
    {
        "Question": "Why are my periods irregular?",
        "Category": "Menstrual Cycle",
        "Subcategory": "Irregular Periods",
        "SeverityLevel": 5,
        "Response": "Irregular periods can be caused by hormonal imbalances, stress, and changes in weight. Consult a doctor if the irregularity persists."
    },
    {
        "Question": "Extreme pain and discomfort (during cycle)",
        "Category": "Menstrual Cycle",
        "Subcategory": "Pain",
        "SeverityLevel": 8,
        "Response": "Extreme pain during your cycle could be a sign of conditions like endometriosis or PCOS. Consult a doctor. In the meantime, lifestyle changes such as stress management and a healthy diet can help."
    },
    {
        "Question": "Abdominal pain but missed cycle",
        "Category": "Menstrual Cycle",
        "Subcategory": "Missed Period",
        "SeverityLevel": 9,
        "Response": "This might be a sign of PCOS. Consult a doctor. Stress and unhealthy eating can result in unusual menstrual cycles. Exercising and maintaining a healthy weight helps irregular flow and PCOS."
    },
    {
        "Question": "Heavy flow/ painful periods/ longer cycles BUT regularity is present",
        "Category": "Menstrual Cycle",
        "Subcategory": "Heavy Flow",
        "SeverityLevel": 7,
        "Response": "For heavy flow and painful periods, consult a doctor if there is major discomfort. Otherwise, maintain a healthy diet, exercise regularly, and manage stress. Using a heating bag and light painkillers can help."
    },
    {
        "Question": "Brown or Blackish blood",
        "Category": "Menstrual Cycle",
        "Subcategory": "Blood Color",
        "SeverityLevel": 5,
        "Response": "Brown or blackish blood is usually due to oxidation. If it happens frequently, consult a doctor to check for fibroids."
    },
    {
        "Question": "White discharge",
        "Category": "Menstrual Cycle",
        "Subcategory": "Discharge",
        "SeverityLevel": 3,
        "Response": "White discharge is normal and helps clean and lubricate your vagina. If it's accompanied by itching or irritation, it could be a sign of infection."
    },
    {
        "Question": "Is pubic hair unhygienic?",
        "Category": "Hygiene",
        "Subcategory": "Pubic Hair",
        "SeverityLevel": 2,
        "Response": "Pubic hair is not unhygienic if you maintain regular washing. It serves important purposes, such as regulating body temperature."
    },
    {
        "Question": "Can I shave my pubic hair?",
        "Category": "Hygiene",
        "Subcategory": "Shaving",
        "SeverityLevel": 2,
        "Response": "You can shave your pubic hair, but avoid shaving during your period as it can cause irritation. Follow proper shaving techniques to avoid infection."
    },
    {
        "Question": "Can I engage in physical activities on my periods?",
        "Category": "Menstrual Cycle",
        "Subcategory": "Physical Activities",
        "SeverityLevel": 1,
        "Response": "Yes, physical activities can help relieve symptoms like cramps and bloating. Adjust the intensity based on how you feel."
    },
    {
        "Question": "Why do I feel fatigue and light headed during that time of the month?",
        "Category": "Menstrual Cycle",
        "Subcategory": "Fatigue",
        "SeverityLevel": 4,
        "Response": "Fatigue and lightheadedness can be due to decreased estrogen levels, iron deficiency, or stress. Ensure you have a balanced diet and enough sleep."
    },
    {
        "Question": "Rashes in private area during periods",
        "Category": "Menstrual Cycle",
        "Subcategory": "Rashes",
        "SeverityLevel": 6,
        "Response": "Rashes can be caused by sanitary products. Use biodegradable, toxin-free pads and avoid sweating. Change sanitary products regularly and wash with water."
    },
    {
        "Question": "Cramps and sore breasts",
        "Category": "Menstrual Cycle",
        "Subcategory": "Symptoms",
        "SeverityLevel": 5,
        "Response": "Cramps and sore breasts are common before your period starts. If discomfort is extreme, consult a doctor. Regularly check for lumps in your breasts."
    },
    {
        "Question": "Will my height stunt after I start menstruating?",
        "Category": "Menstrual Cycle",
        "Subcategory": "Growth",
        "SeverityLevel": 3,
        "Response": "It's typical to grow another 7 cm after menstruation starts. Girls usually stop growing about 2 years after starting their period."
    }
]

def process_user_input(user_input):
    user_tokens = set(word_tokenize(user_input.lower()))
    best_match = None
    max_intersection = 0
    
    for entry in knowledge_base:
        question_tokens = set(word_tokenize(entry["Question"].lower()))
        intersection = len(user_tokens.intersection(question_tokens))
        
        if intersection > max_intersection:
            max_intersection = intersection
            best_match = entry
    
    return best_match

@app.route('/question', methods=['POST'])
def question():
    try:
        data = request.json
        user_input = data.get('question')
        logging.debug(f"Received question: {user_input}")
        matched_entry = process_user_input(user_input)
        
        if matched_entry:
            response = matched_entry["Response"]
            logging.debug(f"Matched response: {response}")
            return jsonify({'response': response})
        else:
            logging.debug("No matching response found")
            return jsonify({'response': "Sorry, I couldn't find a matching response."}), 404
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

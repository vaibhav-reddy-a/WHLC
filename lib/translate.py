import requests

def translate_response(response, target_language):
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': response,
        'target': target_language,
        'key': 'AIzaSyBEy9wGAb_hjKHRKATdOPElUhYsxgv2kaA'
    }
    response = requests.get(url, params=params)
    return response.json()['data']['translations'][0]['translatedText']

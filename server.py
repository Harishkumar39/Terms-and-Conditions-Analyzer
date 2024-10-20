# server.py
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from nltk.stem import WordNetLemmatizer
import joblib
from risk_scores import analyzing_terms_and_conditions

lemmatizer = WordNetLemmatizer()
classifier = joblib.load('model.joblib')


app = Flask(__name__)

@app.route('/read_page', methods=['POST'])
def read_page():
    data = request.json
    tab_url = data['tab']['url']
    response = requests.get(tab_url)
    url=""
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        anchor_tags = soup.find_all('a')
        for anchor_tag in anchor_tags:
            href = anchor_tag.get('href')
            tag_name = lemmatizer.lemmatize(anchor_tag.getText())
            if href:
                if "term" in tag_name or "conditions" in tag_name or 't' in tag_name or 'c' in tag_name:
                    url = href
    else:
        print(response.status_code)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body.text
        resultant = analyzing_terms_and_conditions(body)
        # for key, value in resultant.items():
        #     print(f'{key}\t{value}')
    else:
        print('Error : '+response.status_code)


    # Add your logic here to read the content of the current page (tab_url)
    # You might want to use libraries like requests or BeautifulSoup for web scraping

    result = {'status': 'success', 'message': 'Page read successfully', 'resultant': resultant}
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)

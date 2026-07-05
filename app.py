import os
from flask import Flask, request, jsonify
import joblib
import numpy as np
import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer=WordNetLemmatizer()
stop_words=set(stopwords.words('english'))

load_error_msg = None

# Get the directory where app.py is located so it can find the .pkl files
base_dir = os.path.dirname(os.path.abspath(__file__))

try:
    model_path = os.path.join(base_dir, 'lr_model.pkl')
    vectorizer_path = os.path.join(base_dir, 'tfidf_vectorizer.pkl')
    
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("Model and vector loaded successfully.")
except Exception as e:
    print(f"Error. Model or vectorizer not found: {e}")
    load_error_msg = str(e)
    model = None
    vectorizer = None

def process_text(text):
    text=text.lower()
    text=re.sub(r'<.*?>','',text)
    text=re.sub(r'[^a-zA-Z\s]','',text)
    tokens=text.split()
    cleaned_tokes=[lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(cleaned_tokes)

app=Flask(__name__)


@app.route('/predict',methods=['POST'])
def predict():
    try:
        data=request.get_json()
        if data is None:
            return jsonify({'error':'Invalid input'}),400  
    except Exception as e:
        return jsonify({'error':f'Parsing error occured {str(e)}'}),400
    
    review_text=data.get('review')

    if not review_text or not isinstance(review_text,str) or not review_text.strip():
        return jsonify({'error':'The "review" field is missing'}),400

    cleaned_text=process_text(review_text)

    if vectorizer is None or model is None:
        return jsonify({'error': f'Model failed to load during startup: {load_error_msg}'}), 500

    try:
        text_vector=vectorizer.transform([cleaned_text])
    except Exception as e:
        return jsonify({'error': f'An error occurred during text vectorization: {str(e)}'}), 500
    
    try:
        prediction=model.predict(text_vector)
        sentiment=prediction[0]
    except Exception as e:
        return jsonify({'error': f'An error occurred during model prediction: {str(e)}'}), 500
    
    return jsonify({'sentiment': sentiment.title()}),200

if __name__=='__main__':
    app.run(debug=True, port=5000)
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

pipeline_path = os.path.join('pickle', 'pipeline.pkl')
with open(pipeline_path, 'rb') as f:
    pipeline = pickle.load(f)

def prepare_input_data(form_data):
    furnishing_map = {
        'not-furnished': 0,
        'semi-furnished': 1,
        'furnished': 2
    }
    
    data = {
        'area': [int(form_data.get('area', 0))],
        'bedrooms': [int(form_data.get('bedrooms', 0))],
        'bathrooms': [int(form_data.get('bathrooms', 0))],
        'stories': [int(form_data.get('stories', 1))],
        'mainroad': [int(form_data.get('mainroad', 0))],
        'guestroom': [int(form_data.get('guestroom', 0))],
        'basement': [int(form_data.get('basement', 0))],
        'hotwaterheating': [int(form_data.get('hotwaterheating', 0))],
        'airconditioning': [int(form_data.get('airconditioning', 0))],
        'parking': [int(form_data.get('parking', 0))],
        'prefarea': [int(form_data.get('prefarea', 0))],
        'furnishingstatus': [furnishing_map.get(form_data.get('furnishingstatus', 'not-furnished'), 0)]
    }
    
    df = pd.DataFrame(data)
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    form_data = None
    
    if request.method == 'POST':
        form_data = {
            'area': request.form.get('area'),
            'bedrooms': request.form.get('bedrooms'),
            'bathrooms': request.form.get('bathrooms'),
            'stories': request.form.get('stories'),
            'parking': request.form.get('parking'),
            'mainroad': 1 if request.form.get('mainroad') else 0,
            'guestroom': 1 if request.form.get('guestroom') else 0,
            'basement': 1 if request.form.get('basement') else 0,
            'hotwaterheating': 1 if request.form.get('hotwaterheating') else 0,
            'airconditioning': 1 if request.form.get('airconditioning') else 0,
            'prefarea': 1 if request.form.get('prefarea') else 0,
            'furnishingstatus': request.form.get('furnishingstatus')
        }
        
        try:
            input_df = prepare_input_data(form_data)
            log_prediction = pipeline.predict(input_df)[0]
            prediction = np.expm1(log_prediction)
            prediction = round(prediction, 0)
            prediction_formatted = f"{prediction:,.0f}".replace(",", " ")
        except Exception as e:
            prediction = None
            prediction_formatted = None
            print(f"Ошибка при предсказании: {e}")
        
        return render_template('index.html', form_data=form_data, prediction=prediction_formatted)
    
    return render_template('index.html', form_data=form_data, prediction=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

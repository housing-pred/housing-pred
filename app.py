from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        area = request.form.get('area')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        stories = request.form.get('stories')
        parking = request.form.get('parking')
        mainroad = 1 if request.form.get('mainroad') else 0
        guestroom = 1 if request.form.get('guestroom') else 0
        basement = 1 if request.form.get('basement') else 0
        hotwaterheating = 1 if request.form.get('hotwaterheating') else 0
        airconditioning = 1 if request.form.get('airconditioning') else 0
        prefarea = 1 if request.form.get('prefarea') else 0
        furnishingstatus = request.form.get('furnishingstatus')
        
        form_data = {
            'area': area,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'stories': stories,
            'parking': parking,
            'mainroad': mainroad,
            'guestroom': guestroom,
            'basement': basement,
            'hotwaterheating': hotwaterheating,
            'airconditioning': airconditioning,
            'prefarea': prefarea,
            'furnishingstatus': furnishingstatus
        }
        
        return render_template('index.html', form_data=form_data)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

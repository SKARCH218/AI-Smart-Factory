from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)
model = load_model('your_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    time = data['Time']
    wheel = data['wheel']

    # 예측 수행
    prediction = model.predict(np.array([[time, wheel]]))
    probability = prediction[0][0] * 100  # 0~1 범위의 값이 예측되는 경우

    return jsonify({'probability': probability})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

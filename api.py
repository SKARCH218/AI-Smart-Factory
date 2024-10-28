import pandas as pd
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# 예측 결과를 저장할 CSV 파일 이름
results_file = 'predictions.csv'

@app.route('/save_prediction', methods=['POST'])
def save_prediction():
    data = request.get_json()
    
    # 예측 결과와 함께 필요한 정보를 추출
    failure_probability = data['failure_probability']
    remaining_lifetime = data['remaining_lifetime']
    start_date = data['startDate']
    wheel = data['wheel']

    # 예측 결과를 CSV 파일에 저장
    results = {
        'start_date': start_date,
        'wheel': wheel,
        'failure_probability': failure_probability,
        'remaining_lifetime': remaining_lifetime,
        'prediction_date': datetime.datetime.now().strftime('%Y-%m-%d')
    }

    # 기존 데이터 불러오기 및 추가
    try:
        results_df = pd.read_csv(results_file)
    except FileNotFoundError:
        results_df = pd.DataFrame(columns=results.keys())

    results_df = results_df.append(results, ignore_index=True)
    results_df.to_csv(results_file, index=False)

    return jsonify({'status': 'success', 'message': 'Prediction saved successfully.'}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)

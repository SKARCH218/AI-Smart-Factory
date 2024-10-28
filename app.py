from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta

app = Flask(__name__)
model = load_model('your_model.keras')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    try:
        # 사용 시작 날짜와 현재 날짜 계산
        start_date_str = data['startDate']  # 사용 시작 날짜 (문자열)
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')  # 문자열을 날짜로 변환
        current_date = datetime.now()  # 현재 날짜

        usage_duration = ((current_date - start_date).days) * 24  # 사용  계산

        # 사용 일수가 0 미만인 경우 에러 처리
        # if usage_duration < 0:
        #     usage_duration = (((current_date - start_date).days) * 24) * (-1) # 사용 일수 계산

        if usage_duration < 0:
           return jsonify({'error': '사용 시작 날짜가 미래입니다.'}), 400

        wheel = data['wheel']  # 숫돌 정보

        # 예측을 위한 입력 데이터 준비
        input_data = np.array([[usage_duration, wheel]])
        print(f"{input_data}")
        
        # 모델 예측
        # 모델 예측값 로그로 확인 (디버그용)

        if (wheel == 1):
            prediction = 860 - (model.predict(input_data) / 2500)
            print(f"모델 예측 값: {prediction}, 사용 기간: {usage_duration}시간, 숫돌: A")
        elif (wheel == 2):
            prediction = 977 - (model.predict(input_data) / 2500)
            print(f"모델 예측 값: {prediction}, 사용 기간: {usage_duration}시간, 숫돌: WA")
        elif (wheel == 3):
            prediction = 1038 - (model.predict(input_data) / 2500)
            print(f"모델 예측 값: {prediction}, 사용 기간: {usage_duration}시간, 숫돌: C")
        elif (wheel == 4):
            prediction = 1099 - (model.predict(input_data) / 2500)
            print(f"모델 예측 값: {prediction}, 사용 기간: {usage_duration}시간, 숫돌: GC")

        # 모델 예측값에서 남은 수명 추출
        remaining_lifetime = prediction[0][0] if len(prediction[0]) >= 1 else None
    
        # 예측된 남은 수명이 유효한지 체크
        if remaining_lifetime is None or remaining_lifetime <= 0:
            remaining_lifetime = '오류'
            expected_replacement_date = '오류'
        else:
            # numpy.float32 값을 정수로 변환
            remaining_lifetime = int(remaining_lifetime)
            expected_replacement_date = current_date + timedelta(days=remaining_lifetime)
            expected_replacement_date = expected_replacement_date.strftime('%Y-%m-%d')

        return jsonify({
            'remaining_lifetime': remaining_lifetime,
            'expected_replacement_date': expected_replacement_date
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)

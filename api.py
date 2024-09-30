from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# CSV 파일 경로 설정
csv_file_path = "maintenance_data.csv"

# CSV 파일에 데이터를 추가하는 함수
def append_to_csv(data):
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()  # 파일이 없을 때 헤더 작성
        writer.writerow(data)

# CSV 파일에서 데이터를 읽는 함수
def read_from_csv():
    if not os.path.isfile(csv_file_path):
        return []
    
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

# 예측 유지보수 결과를 POST로 저장하는 엔드포인트
@app.route('/api/save_maintenance', methods=['POST'])
def save_maintenance():
    data = request.json
    append_to_csv(data)
    return jsonify({"message": "Data saved successfully!"}), 200

# 저장된 데이터를 GET으로 불러오는 엔드포인트
@app.route('/api/get_maintenance', methods=['GET'])
def get_maintenance():
    data = read_from_csv()
    return jsonify(data), 200

# API 실행
if __name__ == '__main__':
    app.run(port=5001, debug=True)  # api.py는 5001 포트 사용

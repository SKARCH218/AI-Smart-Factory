끝까지 읽어주세요 !!
제작자: SKARCH

--------------------------------------------------------------

예측 페이지: http://127.0.0.1:5000
API 테스트: http://127.0.0.1:5001/api/get_maintenance

--------------------------------------------------------------

ai.py
인공지능 학습 모델

api.py
HTML 과 통신할 api

app.py
예측 작업 수행

your_model.h5
학습된 모델
0.9945

balanced_tool_data.csv
인공지능 학습자료
y데이터 = 0 or 1 # 교체 여부
x데이터 = # 숫돌 총 사용 시간, 숫돌 종류

templates
- index.html
HTML 웹 페이지

--------------------------------------------------------------

app.py, api.py 를 실행 시켜야 웹사이트에 접속이 됩니다. (반드시 두개 모두 키고있어야 합니다.)

python app.py

python api.py

--------------------------------------------------------------

사용하시기전에 cmd 에서

pip install tensorflow

pip install numpy

pip install pandas

를 입력해서 설치하여주세요!!

import pandas as pd
import numpy as np
import tensorflow as tf

# 데이터 불러오기
data = pd.read_csv('balanced_tool_data.csv')
data = data.dropna()  # 결측치 제거

# y데이터와 x데이터 분리
y데이터 = data['교체'].values
x데이터 = data[['총 사용 시간', '숫돌']].values

# 모델 구성
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='tanh', input_shape=(2,)),
    tf.keras.layers.Dense(128, activation='tanh'),
    tf.keras.layers.Dense(64, activation='tanh'),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])

# 모델 컴파일
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 모델 학습
model.fit(x데이터, y데이터, epochs=10000)

# 모델 저장
model.save('your_model.h5')  # 모델을 저장합니다.

# 나중에 모델 로드
# model = load_model('your_model.h5')  # 저장된 모델을 로드합니다.

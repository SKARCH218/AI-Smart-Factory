import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score

# 데이터 불러오기
data = pd.read_csv('balanced_tool_data.csv')
data = data.dropna()

# 디버깅: 실제 열 이름 출력
print("Columns in the dataset:", data.columns)

# 데이터에서 필요한 부분만 추출
# 공백이 있을 수 있으니 스트립 처리
data.columns = data.columns.str.strip()
y_continuous = data['사용시간'].values  # 남은 수명 (연속적인 값)
x데이터 = data[['교체', '숫돌']].values  # 사용한 일수와 숫돌 종류

# 데이터 스케일링
scaler = StandardScaler()
x데이터_scaled = scaler.fit_transform(x데이터)

# 모델 구성
def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(x데이터_scaled.shape[1],)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')  # 출력층 활성화 함수를 linear로 설정
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='mean_squared_error',  # 손실 함수 수정
                  metrics=['mae'])  # 평균 절대 오차
    return model

# KFold를 이용해 학습 및 평가
kfold = KFold(n_splits=5, shuffle=True)
fold_no = 1
for train_idx, test_idx in kfold.split(x데이터_scaled):
    x_train, x_test = x데이터_scaled[train_idx], x데이터_scaled[test_idx]
    y_train, y_test = y_continuous[train_idx], y_continuous[test_idx]
    
    model = create_model()
    
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
    
    model.fit(x_train, y_train, epochs=100, validation_data=(x_test, y_test), callbacks=[early_stopping, reduce_lr])
    
    scores = model.evaluate(x_test, y_test)
    print(f'Fold {fold_no} MSE: {scores[0]}, MAE: {scores[1]}')
    
    y_pred = model.predict(x_test)
    print(f'R^2 Score for Fold {fold_no}: {r2_score(y_test, y_pred)}')
    
    fold_no += 1
    
# 최종 모델 저장
model.save('your_model.keras')

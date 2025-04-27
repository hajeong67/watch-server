import tensorflow as tf

# 1. Keras 모델 로드 (.h5 파일)
model = tf.keras.models.load_model("best_model_v6.h5")

# 2. TFLiteConverter 사용
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# 3. (선택) 최적화 옵션 적용 – 용량 줄이고 속도 빠르게
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 4. 변환 실행
tflite_model = converter.convert()

# 5. .tflite 파일로 저장
with open("emotion/ml_models/best_model_v6.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ 변환 완료: best_model_v6.tflite")

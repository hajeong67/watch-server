import json
import numpy as np

from django.core.cache import cache
from config import settings
from celery import shared_task
from opensearchpy.exceptions import RequestError

from emotion.ml_models.ppg_model import PPGModel
from users import models as users_models, serializers as users_serializers

from celery import shared_task
import logging
from users.models import Watch # device_id → user 매핑
from preprocess.ppg_preprocess import PpgModelPredictor
import config.settings as settings

logger = logging.getLogger(__name__)
MODEL_PATH = r"C:\Users\user\Desktop\watch-server\watch-server\emotion\ml_models\best_model_v6.h5"
GMM_P_PATH = r"C:\Users\user\Desktop\watch-server\watch-server\emotion\ml_models\gmm_p_v2.pkl"
GMM_N_PATH = r"C:\Users\user\Desktop\watch-server\watch-server\emotion\ml_models\gmm_n_v2.pkl"
PICKLE_PATH = r"C:\Users\user\Desktop\watch-server\watch-server\emotion\ml_models\list_v2.pickle"
CHUNK_SIZE = 300
OVERLAP = 30

predictor = PpgModelPredictor(
    model_path=MODEL_PATH,
    gmm_n_path=GMM_N_PATH,
    gmm_p_path=GMM_P_PATH,
    list_pickle_path=PICKLE_PATH,
    chunk_size=CHUNK_SIZE,
    overlap=OVERLAP
)

# PPG 모델 캐시 로딩
def get_or_restore_ppg_model():
    model = cache.get("ppg_model")
    if not model:
        model = PPGModel(model_path=MODEL_PATH)
        cache.set("ppg_model", model)
    return model

# OpenSearch에 기록할 로깅 포맷
def get_json_log(level, message):
    message['level'] = level
    return json.dumps(message)

# 장치 정보 가져오기
def get_device(device_id):
    try:
        return Watch.objects.select_related("user").get(device_id=device_id)
    except Watch.DoesNotExist:
        return None

def run_ppg_positioning(data):
    device_id = data.get('device_id')
    ppg = data.get('ppg')
    acc = data.get('acc')
    time = data.get('time')

    # try:
    #     watch = Watch.objects.select_related("user").get(device_id=device_id)
    # except Watch.DoesNotExist:
    #     logger.warning(f"Unknown device_id: {device_id}")
    #     return

    watch = Watch.objects.filter(device_id=device_id).first()
    if not watch:
        logger.warning(f"Unknown device_id: {device_id}")
        return

    # PPG 추론
    x_data, pred_list, state, error = predictor.ppg_process_and_predict(ppg)

    if error:
        logger.error(f"PPG 처리 오류: {error}")
        return

    result = {
        "device_id": device_id,
        "user": {
            "id": watch.user.id,
            "username": watch.user.username,
            "email": watch.user.email
        },
        "time": time,
        "ppg": ppg,
        "acc": acc,
        "state": state
    }

    # OpenSearch 저장
    try:
        settings.opensearch_client.index(
            index="logs-ppg-inference",
            body=get_json_log("INFO", result)
        )
    except Exception as e:
        logger.error(f"OpenSearch 저장 실패: {e}")

    logger.info(f"[PPG 추론] 사용자: {watch.user.username}, 상태: {state}")
    return result

def get_json_log(level, message):
    # numpy 타입을 기본 타입으로 바꿔주는 함수
    def convert(obj):
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        return str(obj)  # 예외 방지용

    message['level'] = level
    return json.dumps(message, default=convert)

# # Celery 태스크로 비동기 실행
# @shared_task(ignore_result=True)
# def run_ppg_positioning_task(data):
#     run_ppg_positioning(data)
#
# @shared_task
# def log_demo_task(message):
#     logger.info(f"[TASK] log_demo_task received message: {message}")
#     return f"Logged message: {message}"

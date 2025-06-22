from opensearchpy import OpenSearch
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'config', 'config.json')) as f:
    config = json.load(f)

HOST = config["opensearch"]["host"]
PORT = config["opensearch"]["port"]
AUTH = (config["opensearch"]["auth"]["user"], config["opensearch"]["auth"]["password"])

# OpenSearch 클라이언트 생성
client = OpenSearch(
    hosts=[{"host": HOST, "port": PORT}],  # 엔드포인트 및 포트 설정
    http_auth=AUTH,  # 사용자 인증 정보 적용
    use_ssl=True,  # SSL 사용
    verify_certs=False,  # 인증서 검증 활성화
    ssl_assert_hostname=False,  # 호스트명 검증 비활성화
    ssl_show_warn=False  # SSL 경고 비활성화
)

def is_connected():
    try:
        info = client.info()
        print(f"✅ OpenSearch 연결 성공: {info['cluster_name']}")
        return True
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
        return False
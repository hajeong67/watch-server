from django.test import TestCase

# Create your tests here.
from opensearchpy import OpenSearch

# OpenSearch 클라이언트 설정
HOST = "search-watch-opensearch-domain-y2ayujgu47jvuwgv6vj4wl4et4.ap-northeast-2.es.amazonaws.com"
AUTH = ("hajeong", "Hajeong67!")

client = OpenSearch(
    hosts=[{"host": HOST, "port": 443}],
    http_auth=AUTH,
    use_ssl=True,
    verify_certs=True
)

# 데이터 삽입
data = {
    "time": 1710480000000,  # 예제 타임스탬프
    "device_id": "user_123",
    "acc": {"x": 10, "y": -5, "z": 2},
    "ppg": [100, 102, 105, 107, 110]  # 👈 배열로 저장
}

response = client.index(index="sensor-data", body=data)
print("✅ 데이터 삽입 완료!", response)

query = {
    "query": {
        "match_all": {}  # 모든 데이터 검색
    }
}

response = client.search(index="sensor-data", body=query)
print("📌 저장된 데이터:", response["hits"]["hits"])

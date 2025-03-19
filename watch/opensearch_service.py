from watch.opensearch_client import client

INDEX_NAME = "sensor-data"

# if client.indices.exists(index="sensor-data"):
#     client.indices.delete(index="sensor-data")
#     print("❌ 기존 인덱스 삭제 완료!")
# else:
#     print("✅ 기존 인덱스가 존재하지 않음!")

def create_index():
    body = {
        "settings": {
            "index": {
                "number_of_shards": 4,
                "number_of_replicas": 1  # 복제본 설정 추가
            }
        },
        "mappings": {
            "properties": {
                "time": {"type": "date", "format": "epoch_millis"},
                "device_id": {"type": "keyword"},
                "acc": {
                    "type": "nested",
                    "properties": {
                        "x": {"type": "integer"},
                        "y": {"type": "integer"},
                        "z": {"type": "integer"}
                    }
                },
                "ppg": {
                    "type": "integer",
                    "index": False,
                    "doc_values": True
                }
            }
        }
    }

    if client.indices.exists(index=INDEX_NAME):
        print(f"⚠️ 인덱스 '{INDEX_NAME}' 이미 존재합니다.")
    else:
        response = client.indices.create(index=INDEX_NAME, body=body)
        print(f"✅ 인덱스 '{INDEX_NAME}' 생성 완료! 응답: {response}")

# 인덱스 생성 실행
create_index()

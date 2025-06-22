from watch.opensearch_client import client

INDEX_NAME= "logs-ppg-inference"

# 인덱스 템플릿
def create_index_template():
    template = {
        "index_patterns": [INDEX_NAME, f"{INDEX_NAME}-*"],
        "data_stream": {},
        "template": {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date", "format": "epoch_millis"},
                    "time":      {"type": "date", "format": "epoch_millis"},
                    "device_id": {"type": "keyword"},
                    "acc":       {"type": "object",  "enabled": False},
                    "ppg":       {"type": "integer", "index": False, "doc_values": True},
                    "prediction":{"type": "float"},
                    "user": {
                        "properties": {
                            "id":       {"type": "integer"},
                            "username": {"type": "keyword"},
                            "email":    {"type": "keyword"}
                        }
                    }
                }
            }
        },
        "priority": 500
    }
    client.indices.put_index_template(name="ppg-data-template", body=template)
    print("✅ 인덱스 템플릿 OK")

# 데이터 스트림
def create_data_stream():
    try:
        client.indices.create_data_stream(name=INDEX_NAME)
        print(f"✅ 데이터 스트림 '{INDEX_NAME}' OK")
    except Exception as e:
        if "resource_already_exists_exception" in str(e):
            print(f"⚠️ 데이터 스트림 '{INDEX_NAME}' 이미 존재")
        else:
            raise

def init_opensearch():
    create_index_template()
    create_data_stream()

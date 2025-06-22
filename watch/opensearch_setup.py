from watch.opensearch_client import client

INDEX_ALIAS       = "logs-ppg-inference"
ILM_POLICY_NAME   = "ppg-ilm-policy"

# ILM 정책
def create_ilm_policy():
    policy = {
        "policy": {
            "phases": {
                "hot": {
                    "min_age": "0ms",
                    "actions": {
                        "rollover": {
                            "max_size": "50gb",
                            "max_age": "1d"
                        }
                    }
                },
                "delete": {
                    "min_age": "30d",
                    "actions": { "delete": {} }
                }
            }
        }
    }

    try:
        # 직접 REST API 호출 (OpenSearch >= 1.x, < 2.x 또는 ES 호환성 모드)
        client.transport.perform_request(
            method="PUT",
            url=f"/_ilm/policy/{ILM_POLICY_NAME}",
            body=policy
        )
        print(f"✅ ILM 정책 '{ILM_POLICY_NAME}' OK")
    except Exception as e:
        if "resource_already_exists_exception" in str(e):
            print(f"⚠️ 정책 '{ILM_POLICY_NAME}' 이미 존재")
        else:
            raise

# 인덱스 템플릿
def create_index_template():
    template = {
        "index_patterns": [f"{INDEX_ALIAS}-*"],
        "data_stream": {},
        "template": {
            "settings": {
                "index.lifecycle.name": ILM_POLICY_NAME,
                "index.lifecycle.rollover_alias": INDEX_ALIAS,
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
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
        client.indices.create_data_stream(name=INDEX_ALIAS)
        print(f"✅ 데이터 스트림 '{INDEX_ALIAS}' OK")
    except Exception as e:
        if "resource_already_exists_exception" in str(e):
            print(f"⚠️ 데이터 스트림 '{INDEX_ALIAS}' 이미 존재")
        else:
            raise

def init_opensearch():
    create_ilm_policy()
    create_index_template()
    create_data_stream()

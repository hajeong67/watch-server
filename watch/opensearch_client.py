from opensearchpy import OpenSearch

# OpenSearch 도메인 엔드포인트 설정
HOST = "search-watch-opensearch-domain-y2ayujgu47jvuwgv6vj4wl4et4.ap-northeast-2.es.amazonaws.com"  # OpenSearch 엔드포인트
PORT = 443  # HTTPS 사용

# OpenSearch 인증 정보 (마스터 사용자 계정)
AUTH = ("hajeong", "Hajeong67!")  # 마스터 사용자 계정 정보 입력

# OpenSearch 클라이언트 생성
client = OpenSearch(
    hosts=[{"host": HOST, "port": PORT}],  # 엔드포인트 및 포트 설정
    http_auth=AUTH,  # 사용자 인증 정보 적용
    use_ssl=True,  # SSL 사용
    verify_certs=True,  # 인증서 검증 활성화
    ssl_assert_hostname=False,  # 호스트명 검증 비활성화
    ssl_show_warn=False  # SSL 경고 비활성화
)




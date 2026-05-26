# RAG 검색 파이프라인 함수
from rag.rag_pipeline import answer_with_retrieval


# 저장된 FAISS 벡터DB 경로
vectorstore_path = "data/vectorstore/samsung_report_faiss"

# 테스트 질문
query = "삼성전자 영업이익 전망 알려줘"

# 질문에 대한 관련 문서 검색
result = answer_with_retrieval(query, vectorstore_path, top_k=3)

print("=" * 50)
print(f"질문: {result['question']}")
print("=" * 50)

print("\n[검색된 근거 Context]")
print(result["context"][:3000])

print("\n[출처 Metadata]")
for source in result["sources"]:
    print(source)
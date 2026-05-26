# RAG 답변 생성 함수
from rag.rag_pipeline import answer_with_retrieval


# 저장된 FAISS 벡터DB 경로
vectorstore_path = "data/vectorstore/samsung_report_faiss"

# 테스트 질문
query = "삼성전자 영업이익 전망 알려줘"

# 검색 기반 답변 생성
result = answer_with_retrieval(query, vectorstore_path, top_k=3)

print(result["answer"])
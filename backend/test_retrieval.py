# 저장된 벡터DB 로드 함수
from rag.retriever import load_vectorstore


# 저장된 FAISS 경로
save_path = "data/vectorstore/samsung_report_faiss"

# 벡터DB 로드
vectorstore = load_vectorstore(save_path)

# 사용자 질문
query = "삼성전자 영업이익 전망 알려줘"

# 질문과 유사한 chunk 검색
docs = vectorstore.similarity_search(query, k=3)

print("=" * 50)
print(f"질문: {query}")
print("=" * 50)

# 검색된 chunk 출력
for i, doc in enumerate(docs):
    print(f"\n[검색 결과 {i+1}]")
    print(doc.page_content[:1000])
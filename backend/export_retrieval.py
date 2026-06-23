# Colab LLM 실험에 사용할 retrieval 결과를 JSON으로 저장하는 파일
import json
import os

from rag.rag_pipeline import answer_with_retrieval


# 저장된 FAISS 벡터DB 경로
vectorstore_path = "data/vectorstore/report_faiss"

# 사용자 질문 입력
query = input("질문 입력: ")

# RAG 검색 실행
result = answer_with_retrieval(query, vectorstore_path, top_k=3)

# Colab에 넘길 데이터 정리
export_data = {
    "question": result["question"],
    "company_name": result["company_name"],
    "intents": result["intents"],
    "contexts": result["contexts"],
    "sources": result["sources"],
}

# 저장 폴더 생성
os.makedirs("data/processed", exist_ok=True)

# 저장할 파일 경로
output_path = "data/processed/retrieval_result.json"

# JSON 파일 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print("retrieval 결과 저장 완료")
print(f"질문: {query}")
print(f"회사: {result['company_name']}")
print(f"저장 위치: {output_path}")
# Colab에서 LLM 실험에 사용할 retrieval 결과를 JSON으로 저장하는 파일
import json

from rag.rag_pipeline import answer_with_retrieval


# 저장된 FAISS 벡터DB 경로
vectorstore_path = "data/vectorstore/report_faiss"

# Colab에서 실험할 질문
query = "현대차 영업이익 알려줘"

# RAG 검색 실행
result = answer_with_retrieval(query, vectorstore_path, top_k=3)

# Colab에 넘길 핵심 데이터만 정리
export_data = {
    "question": result["question"],
    "company_name": result["company_name"],
    "contexts": result["contexts"],
    "sources": result["sources"],
}

# 저장할 파일 경로
output_path = "data/processed/retrieval_result.json"

# JSON 파일로 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print("retrieval 결과 저장 완료")
print(f"저장 위치: {output_path}")
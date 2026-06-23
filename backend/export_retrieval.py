import json
import os

from rag.rag_pipeline import answer_with_retrieval

vectorstore_path = "data/vectorstore/report_faiss"

print("삼성전자 RAG 테스트")
print("종료하려면 q 입력")
print("=" * 50)

while True:
    query = input("\n질문 입력: ")

    if query.lower() == "q":
        break

    result = answer_with_retrieval(
        query,
        vectorstore_path,
        top_k=3
    )

    print("\n[검색된 Context]")
    print("-" * 50)

    for i, context in enumerate(result["contexts"]):
        print(f"\nContext {i+1}")
        print(context[:1000])

    print("\n[출처]")
    print("-" * 50)

    for source in result["sources"]:
        print(source)

    export_data = {
        "question": result["question"],
        "company_name": result["company_name"],
        "intents": result["intents"],
        "contexts": result["contexts"],
        "sources": result["sources"],
    }

    os.makedirs("data/processed", exist_ok=True)

    with open(
        "data/processed/retrieval_result.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            export_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\nretrieval_result.json 저장 완료")
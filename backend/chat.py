# 터미널에서 질문을 입력받아 RAG 검색 답변을 출력하는 실행 파일
from rag.rag_pipeline import answer_with_retrieval


# 여러 리포트를 합쳐 저장한 FAISS 벡터DB 경로
vectorstore_path = "data/vectorstore/report_faiss"


print("증권 리포트 기반 회사 전망 RAG 챗봇")
print("종료하려면 q 또는 quit 입력")
print("=" * 50)

while True:
    # 사용자 질문 입력
    query = input("\n질문 입력: ")

    # 종료 명령 처리
    if query.lower() in ["q", "quit"]:
        print("챗봇을 종료합니다.")
        break

    # 검색 기반 답변 생성
    result = answer_with_retrieval(query, vectorstore_path, top_k=3)

    print("\n" + "=" * 50)
    print(result["answer"])
    print("=" * 50)
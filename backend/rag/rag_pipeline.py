# 저장된 벡터DB를 불러오는 함수
from rag.retriever import load_vectorstore


def answer_with_retrieval(query, vectorstore_path, top_k=3):
    # 저장된 FAISS 벡터DB 로드
    vectorstore = load_vectorstore(vectorstore_path)

    # 질문과 관련 있는 chunk 검색
    docs = vectorstore.similarity_search(query, k=top_k)

    # 검색된 chunk를 답변 근거로 정리
    contexts = []
    sources = []

    for doc in docs:
        # 검색된 본문 내용 저장
        contexts.append(doc.page_content)

        # PDF 출처, 페이지 정보 저장
        sources.append({
    "company_name": doc.metadata.get("company_name"),
    "report_date": doc.metadata.get("report_date"),
    "securities_firm": doc.metadata.get("securities_firm"),
    "source": doc.metadata.get("source"),
    "page": doc.metadata.get("page_label")
})

    # 아직 LLM 연결 전이므로 검색 근거를 기반으로 단순 답변 생성
    answer = make_simple_answer(query, contexts, sources)

    return {
        "question": query,
        "answer": answer,
        "contexts": contexts,
        "sources": sources
    }


def make_simple_answer(query, contexts, sources):
    # 검색된 chunk 중 첫 번째 결과를 가장 관련 높은 근거로 사용
    main_context = contexts[0]

    # 사용자가 볼 수 있는 기본 답변 형식 생성
    answer = f"""
질문: {query}

검색된 증권 리포트 내용을 기준으로 보면, 아래 내용이 질문과 가장 관련 있는 근거입니다.

[핵심 근거]
{main_context[:1200]}

[출처]
"""
    # 검색된 문서의 출처 페이지를 함께 표시
    
    for source in sources:
        answer += (
            f"- {source['company_name']} / "
            f"{source['securities_firm']} / "
            f"{source['report_date']} / "
            f"page {source['page']}\n"
            )
        return answer
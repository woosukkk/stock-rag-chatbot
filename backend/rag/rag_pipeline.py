# 저장된 벡터DB를 불러오는 함수
from rag.retriever import load_vectorstore


# 질문 안에서 회사명 key 감지
def detect_company(query):
    # 파일명/metadata와 맞추기 위해 영어 key 기준 사용
    companies = [
        "samsung",
        "hyundai",
        "skhynix",
        "lgenergy"
    ]

    # 대소문자 차이를 무시하고 회사명 key가 질문에 포함되어 있는지 확인
    for company in companies:
        if company.lower() in query.lower():
            return company

    return None


def answer_with_retrieval(query, vectorstore_path, top_k=3):
    # 저장된 FAISS 벡터DB 로드
    vectorstore = load_vectorstore(vectorstore_path)

    # 질문 안에서 회사명 key 찾기
    company_name = detect_company(query)

    # 회사명 key가 있으면 해당 회사 문서만 검색
    if company_name:
        docs = vectorstore.similarity_search(
            query,
            k=top_k,
            filter={"company_name": company_name}
        )

    # 회사명 key가 없으면 전체 문서 검색
    else:
        docs = vectorstore.similarity_search(
            query,
            k=top_k
        )

    # 검색된 chunk 내용 저장
    contexts = []

    # 출처 정보 저장
    sources = []

    for doc in docs:
        # 검색된 본문 저장
        contexts.append(doc.page_content)

        # metadata 기반 출처 정보 저장
        sources.append({
            "company_name": doc.metadata.get("company_name"),
            "report_date": doc.metadata.get("report_date"),
            "securities_firm": doc.metadata.get("securities_firm"),
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page_label")
        })

    # 검색된 내용을 기반으로 답변 생성
    answer = make_simple_answer(query, contexts, sources)

    return {
        "question": query,
        "company_name": company_name,
        "answer": answer,
        "contexts": contexts,
        "sources": sources
    }


def make_simple_answer(query, contexts, sources):
    # 검색 결과가 없는 경우 오류 대신 안내 메시지 반환
    if not contexts:
        return f"""
질문: {query}

해당 회사와 관련된 검색 결과를 찾지 못했습니다.
질문에 입력한 회사명 key와 PDF 파일명에서 추출된 company_name metadata가 일치하는지 확인해주세요.

예시 질문:
- samsung 전망 알려줘
- hyundai 영업이익 전망 알려줘
- skhynix 매출 전망 알려줘
"""

    # 가장 관련도가 높은 첫 번째 chunk 사용
    main_context = contexts[0]

    # 사용자에게 보여줄 답변 생성
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
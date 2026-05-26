# 저장된 벡터DB를 불러오는 함수
from rag.retriever import load_vectorstore


# 질문 안에서 회사명 key 감지
def detect_company(query):
    # 사용자 입력 회사명과 내부 metadata key를 매핑
    company_aliases = {
        "samsung": ["samsung", "삼성전자", "삼성"],
        "hyundai": ["hyundai", "현대차", "현대자동차"],
        "skhynix": ["skhynix", "SK하이닉스", "하이닉스"],
        "lgenergy": ["lgenergy", "LG에너지솔루션", "엘지에너지솔루션"]
    }

    # 대소문자 차이를 무시하기 위해 소문자로 변환
    lower_query = query.lower()

    # 질문 안에 alias가 포함되어 있으면 내부 key 반환
    for company_key, aliases in company_aliases.items():
        for alias in aliases:
            if alias.lower() in lower_query:
                return company_key

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


def extract_important_lines(context):
    # 검색된 chunk에서 답변에 필요한 핵심 줄만 뽑기 위한 키워드
    keywords = [
        "영업이익",
        "매출액",
        "목표주가",
        "투자의견",
        "전망",
        "성장",
        "증가",
        "감소",
        "개선",
        "BUY",
        "Maintain"
    ]

    important_lines = []

    # chunk를 줄 단위로 나누어 확인
    lines = context.split("\n")

    for line in lines:
        clean_line = line.strip()

        # 빈 줄은 제외
        if not clean_line:
            continue

        # 핵심 키워드가 포함된 줄만 저장
        for keyword in keywords:
            if keyword in clean_line:
                important_lines.append(clean_line)
                break

    return important_lines


def make_simple_answer(query, contexts, sources):
    # 검색 결과가 없는 경우 오류 대신 안내 메시지 반환
    if not contexts:
        return f"""
질문: {query}

해당 회사와 관련된 검색 결과를 찾지 못했습니다.
질문에 입력한 회사명과 PDF 파일명에서 추출된 company_name metadata가 일치하는지 확인해주세요.

예시 질문:
- 삼성전자 전망 알려줘
- 현대차 영업이익 전망 알려줘
- skhynix 매출 전망 알려줘
"""

    # 가장 관련도가 높은 첫 번째 chunk 사용
    main_context = contexts[0]

    # 검색된 chunk에서 핵심 줄만 추출
    important_lines = extract_important_lines(main_context)

    # 핵심 줄이 없으면 기존 chunk 일부를 fallback으로 사용
    if important_lines:
        evidence_text = "\n".join(important_lines[:10])
    else:
        evidence_text = main_context[:1200]

    # 사용자에게 보여줄 답변 생성
    answer = f"""
질문: {query}

검색된 증권 리포트 내용을 기준으로 핵심 내용을 정리하면 다음과 같습니다.

[핵심 근거]
{evidence_text}

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
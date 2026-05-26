# 저장된 벡터DB를 불러오는 함수
from rag.retriever import load_vectorstore


def detect_company(query):
    # 사용자 입력 회사명과 내부 metadata key를 매핑
    company_aliases = {
        "samsung": ["samsung", "삼성전자", "삼성"],
        "hyundai": ["hyundai", "현대차", "현대자동차"],
        "skhynix": ["skhynix", "SK하이닉스", "하이닉스"],
        "lgenergy": ["lgenergy", "LG에너지솔루션", "엘지에너지솔루션"],
    }

    lower_query = query.lower()

    for company_key, aliases in company_aliases.items():
        for alias in aliases:
            if alias.lower() in lower_query:
                return company_key

    return None


def detect_intents(query):
    # 질문 유형을 대략적으로 분류
    intent_keywords = {
        "operating_profit": ["영업이익", "영업이익률"],
        "revenue": ["매출액", "매출"],
        "target_price": ["목표주가", "적정주가", "업사이드", "upside"],
        "investment_opinion": ["투자의견", "매수", "buy", "maintain"],
        "hev": ["hev", "하이브리드", "친환경차", "mix"],
        "exchange_rate": ["환율", "usd", "krw", "달러"],
        "performance": ["실적", "분기", "review", "1q"],
        "outlook": ["전망", "성장", "개선", "회복", "기대"],
    }

    lower_query = query.lower()
    intents = []

    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword.lower() in lower_query:
                intents.append(intent)
                break

    return intents


def get_intent_keywords(intents):
    # 특정 리포트에만 과하게 맞추지 않도록 일반적인 키워드만 사용
    keyword_map = {
        "operating_profit": ["영업이익", "영업이익률", "실적", "손익계산서"],
        "revenue": ["매출액", "매출", "실적"],
        "target_price": ["목표주가", "적정주가", "Upside", "Valuation"],
        "investment_opinion": ["투자의견", "BUY", "Buy", "Maintain"],
        "hev": ["HEV", "Mix", "하이브리드", "친환경차", "도매판매"],
        "exchange_rate": ["환율", "USD/KRW", "외화", "원재료비"],
        "performance": ["실적", "Review", "매출액", "영업이익", "YoY", "QoQ"],
        "outlook": ["전망", "기대", "개선", "성장", "회복"],
    }

    keywords = []

    for intent in intents:
        keywords.extend(keyword_map.get(intent, []))

    return list(dict.fromkeys(keywords))


def rerank_docs(docs, intents):
    # FAISS 검색 결과를 약하게 재정렬
    # 너무 강한 점수는 특정 테스트 문서에 오버피팅될 수 있으므로 피함
    intent_keywords = get_intent_keywords(intents)

    if not intent_keywords:
        return docs

    scored_docs = []

    for index, doc in enumerate(docs):
        content = doc.page_content
        score = 0

        # 기존 FAISS 유사도 순서를 기본적으로 존중
        score += max(0, 50 - index)

        # 질문 유형 키워드가 포함된 chunk에 약한 가산점 부여
        for keyword in intent_keywords:
            if keyword in content:
                score += 20

        # 핵심 재무표/실적표로 보이는 chunk에는 약한 가산점
        general_financial_keywords = [
            "연결기준 실적",
            "포괄손익계산서",
            "투자지표",
            "매출액",
            "영업이익",
            "목표주가",
            "투자의견",
        ]

        for keyword in general_financial_keywords:
            if keyword in content:
                score += 5

        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [doc for score, doc in scored_docs]


def answer_with_retrieval(query, vectorstore_path, top_k=3):
    # 저장된 FAISS 벡터DB 로드
    vectorstore = load_vectorstore(vectorstore_path)

    # 회사명과 질문 유형 감지
    company_name = detect_company(query)
    intents = detect_intents(query)

    # 재정렬을 위해 top_k보다 넉넉하게 검색
    search_k = max(top_k * 6, 15)

    if company_name:
        docs = vectorstore.similarity_search(
            query,
            k=search_k,
            filter={"company_name": company_name},
        )
    else:
        docs = vectorstore.similarity_search(
            query,
            k=search_k,
        )

    # 질문 유형 키워드를 기준으로 약하게 재정렬
    docs = rerank_docs(docs, intents)

    # 최종 사용할 문서 개수 제한
    docs = docs[:top_k]

    contexts = []
    sources = []

    for doc in docs:
        contexts.append(doc.page_content)

        sources.append({
            "company_name": doc.metadata.get("company_name"),
            "report_date": doc.metadata.get("report_date"),
            "securities_firm": doc.metadata.get("securities_firm"),
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page_label"),
        })

    answer = make_simple_answer(query, contexts, sources, intents)

    return {
        "question": query,
        "company_name": company_name,
        "intents": intents,
        "answer": answer,
        "contexts": contexts,
        "sources": sources,
    }


def extract_important_lines(context, intents=None):
    # 질문 유형에 맞는 핵심 줄을 추출
    intent_keywords = get_intent_keywords(intents or [])

    default_keywords = [
        "영업이익",
        "영업이익률",
        "매출액",
        "목표주가",
        "투자의견",
        "전망",
        "성장",
        "증가",
        "감소",
        "개선",
        "BUY",
        "Buy",
        "Maintain",
        "순이익",
        "EPS",
        "PER",
        "PBR",
        "ROE",
        "EBITDA",
        "YoY",
        "QoQ",
        "HEV",
        "Mix",
        "친환경차",
        "환율",
        "USD/KRW",
    ]

    keywords = list(dict.fromkeys(intent_keywords + default_keywords))
    important_lines = []

    for line in context.split("\n"):
        clean_line = line.strip()

        if not clean_line:
            continue

        for keyword in keywords:
            if keyword in clean_line:
                important_lines.append(clean_line)
                break

    return important_lines


def make_simple_answer(query, contexts, sources, intents=None):
    if not contexts:
        return f"""
질문: {query}

해당 회사와 관련된 검색 결과를 찾지 못했습니다.
질문에 입력한 회사명과 PDF 파일명에서 추출된 company_name metadata가 일치하는지 확인해주세요.
"""

    all_important_lines = []

    for context in contexts:
        lines = extract_important_lines(context, intents)
        all_important_lines.extend(lines)

    # 중복 줄 제거
    all_important_lines = list(dict.fromkeys(all_important_lines))

    if all_important_lines:
        evidence_text = "\n".join(all_important_lines[:12])
    else:
        evidence_text = contexts[0][:1200]

    answer = f"""
질문: {query}

검색된 증권 리포트 내용을 기준으로 핵심 내용을 정리하면 다음과 같습니다.

[핵심 근거]
{evidence_text}

[출처]
"""

    for source in sources:
        answer += (
            f"- {source['company_name']} / "
            f"{source['securities_firm']} / "
            f"{source['report_date']} / "
            f"page {source['page']}\n"
        )

    return answer
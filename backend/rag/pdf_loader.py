# PDF 파일을 읽기 위한 LangChain 로더
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path, company_name=None, report_date=None, securities_firm=None):
    # PDF 로더 생성
    loader = PyPDFLoader(pdf_path)

    # PDF 전체 페이지 로드
    documents = loader.load()

    # 각 페이지 문서에 추가 metadata 저장
    # 나중에 회사명, 리포트 날짜, 증권사 기준으로 검색/필터링할 때 사용
    for doc in documents:
        doc.metadata["company_name"] = company_name
        doc.metadata["report_date"] = report_date
        doc.metadata["securities_firm"] = securities_firm

    return documents
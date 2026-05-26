# PDF 파일을 읽기 위한 LangChain 로더
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path):
    # PDF 로더 생성
    loader = PyPDFLoader(pdf_path)

    # PDF 전체 페이지 로드
    documents = loader.load()

    return documents
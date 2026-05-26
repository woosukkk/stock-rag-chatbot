# 긴 문서를 RAG 검색에 적합한 작은 단위로 나누기 위한 splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    # chunk_size: 한 조각의 최대 글자 수
    # chunk_overlap: 앞뒤 chunk가 겹치는 글자 수
    # overlap을 주면 문맥이 끊기는 문제를 줄일 수 있음
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    # PDF에서 읽은 페이지 문서들을 여러 chunk로 분리
    chunks = text_splitter.split_documents(documents)

    return chunks
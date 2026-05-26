# 저장된 벡터DB를 불러오는 함수
from rag.retriever import load_vectorstore


def answer_with_retrieval(query, vectorstore_path, top_k=3):
    # 저장된 FAISS 벡터DB 로드
    vectorstore = load_vectorstore(vectorstore_path)

    # 질문과 관련 있는 chunk 검색
    docs = vectorstore.similarity_search(query, k=top_k)

    # 검색된 문서 내용을 하나의 context로 합치기
    context = "\n\n".join([doc.page_content for doc in docs])

    # 아직 LLM 연결 전이므로 검색 근거만 반환
    result = {
        "question": query,
        "context": context,
        "sources": [doc.metadata for doc in docs]
    }

    return result
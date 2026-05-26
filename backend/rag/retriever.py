# 저장된 FAISS 벡터DB를 다시 불러오기 위한 모듈
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_vectorstore(save_path):
    # vector 생성 때 사용한 embedding 모델과 동일해야 함
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # 저장된 FAISS 벡터DB 로드
    vectorstore = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore
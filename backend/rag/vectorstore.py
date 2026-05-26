# 로컬 HuggingFace embedding 모델 사용
# OpenAI API 없이 내 컴퓨터에서 chunk를 벡터로 변환할 수 있음
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_vectorstore(chunks):
    # 한국어/영어 문장 embedding에 사용할 무료 로컬 모델
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # chunk들을 embedding하여 FAISS 벡터DB 생성
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


def save_vectorstore(vectorstore, save_path):
    # 생성된 FAISS 벡터DB를 로컬 폴더에 저장
    vectorstore.save_local(save_path)
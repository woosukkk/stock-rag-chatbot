# 여러 PDF 리포트를 한 번에 벡터DB로 만드는 파일

import os

# PDF 로드
from rag.pdf_loader import load_pdf

# chunk 분리
from rag.chunker import split_documents

# FAISS 생성 및 저장
from rag.vectorstore import create_vectorstore, save_vectorstore


# PDF 파일이 저장된 폴더
raw_data_path = "data/raw"

# 최종 저장될 벡터DB 경로
save_path = "data/vectorstore/report_faiss"


# 모든 문서를 저장할 리스트
all_documents = []


# raw 폴더 안 PDF 파일 순회
for file_name in os.listdir(raw_data_path):

    # PDF 파일만 처리
    if file_name.endswith(".pdf"):

        pdf_path = os.path.join(raw_data_path, file_name)

        print(f"PDF 로드 중: {file_name}")

        # 현재는 파일명 기준으로 회사명 설정
        company_name = file_name.split("_")[0]

        # PDF 로드
        documents = load_pdf(
            pdf_path,
            company_name=company_name,
            report_date="2026-04-08",
            securities_firm="키움증권"
        )

        # 전체 문서 리스트에 추가
        all_documents.extend(documents)


print(f"\n총 문서 수: {len(all_documents)}")


# 전체 문서를 chunk 단위로 분리
chunks = split_documents(all_documents)

print(f"총 chunk 수: {len(chunks)}")


# FAISS 벡터DB 생성
vectorstore = create_vectorstore(chunks)

# 저장
save_vectorstore(vectorstore, save_path)

print("\n벡터DB 저장 완료")
# PDF 로드 함수
from rag.pdf_loader import load_pdf

# 문서 chunk 분리 함수
from rag.chunker import split_documents

# FAISS 벡터DB 생성 및 저장 함수
from rag.vectorstore import create_vectorstore, save_vectorstore


# 테스트할 PDF 파일 경로
pdf_path = "data/raw/samsung_report.pdf"

# FAISS 벡터DB 저장 경로
save_path = "data/vectorstore/samsung_report_faiss"

# PDF 로드
documents = load_pdf(
    pdf_path,
    company_name="삼성전자",
    report_date="2026-04-08",
    securities_firm="키움증권"
)

# 문서를 chunk 단위로 분리
chunks = split_documents(documents)

# chunk를 embedding하여 FAISS 벡터DB 생성
vectorstore = create_vectorstore(chunks)

# 생성한 벡터DB 저장
save_vectorstore(vectorstore, save_path)

print("FAISS 벡터DB 저장 완료")
print(f"저장 위치: {save_path}")
print(f"저장된 chunk 수: {len(chunks)}")
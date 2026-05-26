# PDF 로드 함수
from rag.pdf_loader import load_pdf

# 문서 chunk 분리 함수
from rag.chunker import split_documents


# 테스트할 PDF 파일 경로
pdf_path = "data/raw/samsung_report.pdf"

# PDF 문서를 페이지 단위로 로드
documents = load_pdf(
    pdf_path,
    company_name="삼성전자",
    report_date="2026-04-08",
    securities_firm="키움증권"
)

# 페이지 문서를 검색용 chunk 단위로 분리
chunks = split_documents(documents)

# 생성된 chunk 개수 확인
print(f"총 chunk 수: {len(chunks)}")

print("=" * 50)

# 첫 번째 chunk 내용 일부 출력
print(chunks[0].page_content[:1000])
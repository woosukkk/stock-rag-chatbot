# PDF 로드 함수 가져오기
from rag.pdf_loader import load_pdf


# 테스트할 PDF 경로
pdf_path = "data/raw/samsung_report.pdf"

# PDF 문서 로드
documents = load_pdf(pdf_path)

# 페이지 개수 출력
print(f"총 페이지 수: {len(documents)}")

print("=" * 50)

# 첫 페이지 내용 일부 출력
print(documents[0].page_content[:1000])
import fitz
class PDFTextLoader:
    def load(self, content: bytes):
        try:
            doc = fitz.open(stream=content, filetype="pdf")
        except Exception as exc:
            raise ValueError("The uploaded file is not a readable PDF.") from exc
        pages = []
        try:
            for n, page in enumerate(doc, 1):
                text = page.get_text("text").strip()
                if text: pages.append({"page": n, "text": text})
        finally:
            doc.close()
        if not pages:
            raise ValueError("No selectable text found. Scanned PDFs need OCR, which is not enabled.")
        return pages

import re
def clean_text(text):
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

class TextChunker:
    def __init__(self, chunk_size=900, overlap=150):
        if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
            raise ValueError("Require chunk_size > overlap >= 0.")
        self.chunk_size, self.overlap = chunk_size, overlap
    def split_pages(self, pages):
        output = []
        for page in pages:
            text, start = clean_text(page["text"]), 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                if end < len(text):
                    boundary = text.rfind(" ", start + int(self.chunk_size*.65), end)
                    if boundary > start: end = boundary
                part = text[start:end].strip()
                if part:
                    output.append({"page":page["page"],"text":part,"start_char":start,"end_char":end})
                if end >= len(text): break
                start = max(end-self.overlap, start+1)
        return output

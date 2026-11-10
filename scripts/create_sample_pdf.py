from pathlib import Path
import fitz
out=Path("data/sample_research_note.pdf"); out.parent.mkdir(parents=True,exist_ok=True)
doc=fitz.open(); page=doc.new_page()
page.insert_text((72,72),
"Research Note: Retrieval-Augmented Generation\n\n"
"Retrieval-Augmented Generation (RAG) combines information retrieval with language generation. "
"A retriever searches a collection of documents and returns relevant passages. A language model "
"uses those passages as context to answer a question.\n\n"
"Chunking divides long documents into smaller passages. Overlap can preserve context across chunk "
"boundaries. Each chunk should retain metadata such as document name and page number for citations.",
fontsize=11)
doc.save(out); doc.close(); print(f"Created {out}")

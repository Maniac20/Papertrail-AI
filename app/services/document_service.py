import uuid
from app.ingestion.pdf_loader import PDFTextLoader
from app.ingestion.chunker import TextChunker

class DocumentService:
    def __init__(self, repository, loader, chunker, embeddings, vector_store):
        self.repository,self.loader,self.chunker=repository,loader,chunker
        self.embeddings,self.vector_store=embeddings,vector_store
    def ingest_pdf(self, content, filename, user_id):
        pages=self.loader.load(content)
        chunks=self.chunker.split_pages(pages)
        if not chunks: raise ValueError("No text could be indexed.")
        vectors=self.embeddings.embed_documents([c["text"] for c in chunks])
        document_id=str(uuid.uuid4())
        self.vector_store.upsert_chunks(document_id,user_id,filename,chunks,vectors)
        stamp=self.repository.create(document_id,user_id,filename,len(pages),len(chunks))
        return {"document_id":document_id,"filename":filename,"pages":len(pages),
                "chunks":len(chunks),"uploaded_at":stamp}
    def list_documents(self,user_id):
        return self.repository.list_for_user(user_id)
    def delete_document(self,document_id,user_id):
        if not self.repository.get_for_user(document_id,user_id): return False
        self.vector_store.delete_document(document_id,user_id)
        return self.repository.delete_for_user(document_id,user_id)

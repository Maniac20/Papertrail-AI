from functools import lru_cache
from app.core.config import get_settings
from app.db.sqlite import DocumentRepository
from app.ingestion.pdf_loader import PDFTextLoader
from app.ingestion.chunker import TextChunker
from app.retrieval.embeddings import EmbeddingService
from app.retrieval.vector_store import QdrantVectorStore
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService
from app.services.answer_service import AnswerService
from app.services.query_service import QueryService

@lru_cache
def get_components():
    s=get_settings(); s.prepare_directories()
    embeddings=EmbeddingService(s.embedding_model)
    vectors=QdrantVectorStore(s.qdrant_path,"document_chunks",s.embedding_dimension)
    repo=DocumentRepository(s.sqlite_path)
    docs=DocumentService(repo,PDFTextLoader(),TextChunker(s.chunk_size,s.chunk_overlap),embeddings,vectors)
    docs.max_upload_bytes=s.max_upload_mb*1024*1024
    query=QueryService(RAGService(embeddings,vectors),AnswerService())
    return docs,query

def get_document_service(): return get_components()[0]
def get_query_service(): return get_components()[1]

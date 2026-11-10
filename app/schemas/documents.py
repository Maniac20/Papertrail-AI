from pydantic import BaseModel
class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    pages: int
    chunks: int
    message: str
class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    pages: int
    chunks: int
    uploaded_at: str
class DocumentListResponse(BaseModel):
    documents: list[DocumentInfo]

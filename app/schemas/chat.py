from pydantic import BaseModel, ConfigDict, Field
class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=3, max_length=5000)
    user_id: str = Field(default="demo-user", min_length=1, max_length=100)
    document_ids: list[str] | None = None
class Citation(BaseModel):
    document_id: str
    filename: str
    page: int
    chunk_id: str
    quote: str | None = None
class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_chunks: int
    grounded: bool

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "openai/gpt-oss-20b"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    qdrant_path: str = "./data/qdrant"
    sqlite_path: str = "./data/app.db"
    max_upload_mb: int = 25
    chunk_size: int = 900
    chunk_overlap: int = 150
    retrieval_top_k: int = 6
    retrieval_score_threshold: float = 0.20
    max_context_chars: int = 12000
    request_timeout_seconds: float = 45.0
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def prepare_directories(self):
        for p in [self.qdrant_path, str(Path(self.sqlite_path).parent)]:
            Path(p).mkdir(parents=True, exist_ok=True)

@lru_cache
def get_settings():
    return Settings()

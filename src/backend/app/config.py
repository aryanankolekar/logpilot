from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # ---- Paths ----
    LOG_DIR: Path = Path("data/logs")  # monitored log directory
    VECTOR_STORE_PATH: Path = Path("data/vector_store")  # FAISS + metadata path

    # ---- Models ----
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_ENDPOINT: str = "http://localhost:11434/api/chat"
    LLM_MODEL: str = "llama3.2"

    # ---- Server ----
    HOST: str = "0.0.0.0"
    PORT: int = 6969

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
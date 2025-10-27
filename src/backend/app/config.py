from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_DIR: Path = Path("./data/logs")        # local logs directory
    VECTOR_DIR: Path = Path("./data/vectors")  # FAISS + metadata store
    EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 512
    HOST: str = "0.0.0.0"
    PORT: int = 6969


settings = Settings()

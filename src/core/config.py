import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Automatically load .env from root workspace
load_dotenv()

@dataclass
class AppConfig:
    """Application configuration settings."""
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    artifacts_dir: Path = base_dir / "artifacts"
    prototype_dir: Path = base_dir / "prototype"
    
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    preferred_model: str = os.getenv("OLLAMA_MODEL", "hermes3:8b")
    fallback_model: str = os.getenv("OLLAMA_FALLBACK_MODEL", "qwen2.5:7b")
    
    ollama_num_gpu: int = int(os.getenv("OLLAMA_NUM_GPU", "99"))
    ollama_num_ctx: int = int(os.getenv("OLLAMA_NUM_CTX", "2048"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))

    def ensure_directories(self):
        """Creates artifacts and prototype directories if they do not exist."""
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.prototype_dir.mkdir(parents=True, exist_ok=True)

def get_config() -> AppConfig:
    """Returns singleton-like application configuration."""
    cfg = AppConfig()
    cfg.ensure_directories()
    return cfg

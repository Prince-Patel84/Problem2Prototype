from typing import Optional, Generator
from langchain_ollama import ChatOllama
from .config import AppConfig, get_config

class LLMService:
    """Manages ChatOllama connections, GPU offloading, fallbacks, and invocation/streaming helpers."""
    
    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or get_config()
        self.active_model_name = self.config.preferred_model
        self.client = self._initialize_client()

    def _initialize_client(self) -> ChatOllama:
        """Attempts to initialize the primary Ollama model with GPU offload, falling back if needed."""
        try:
            client = ChatOllama(
                model=self.config.preferred_model,
                base_url=self.config.ollama_base_url,
                temperature=self.config.temperature,
                num_gpu=self.config.ollama_num_gpu,
                num_ctx=self.config.ollama_num_ctx
            )
            # Lightweight probe
            client.invoke("test")
            self.active_model_name = self.config.preferred_model
            return client
        except Exception as e:
            print(f"[!] Primary model '{self.config.preferred_model}' failed ({e}). Falling back to '{self.config.fallback_model}'...")
            client = ChatOllama(
                model=self.config.fallback_model,
                base_url=self.config.ollama_base_url,
                temperature=self.config.temperature,
                num_gpu=self.config.ollama_num_gpu,
                num_ctx=self.config.ollama_num_ctx
            )
            self.active_model_name = self.config.fallback_model
            return client

    def invoke(self, system_prompt: str, user_content: str) -> str:
        """Executes a standard system + user prompt pair synchronously."""
        response = self.client.invoke([
            ("system", system_prompt),
            ("user", user_content)
        ])
        return str(response.content)

    def stream(self, system_prompt: str, user_content: str) -> Generator[str, None, None]:
        """Streams response tokens in real-time as a Python generator."""
        chunks = self.client.stream([
            ("system", system_prompt),
            ("user", user_content)
        ])
        for chunk in chunks:
            yield str(chunk.content)

    def refine(self, original_output: str, user_feedback: str, role_title: str = "Senior Software Engineering Specialist") -> str:
        """Refines existing output incorporating direct human feedback synchronously."""
        refinement_system_prompt = (
            f"Role: {role_title}\n"
            "Task: You are surgically refining the previous output based on direct user feedback. "
            "Strictly incorporate the user's feedback into the output while maintaining clean, structured formatting. "
            "Preserve all existing valid data while applying the requested revisions."
        )
        refinement_user_prompt = f"Original Output:\n{original_output}\n\nUser Feedback:\n{user_feedback}"
        return self.invoke(refinement_system_prompt, refinement_user_prompt)

    def stream_refine(self, original_output: str, user_feedback: str, role_title: str = "Senior Software Engineering Specialist") -> Generator[str, None, None]:
        """Streams refined output tokens in real-time."""
        refinement_system_prompt = (
            f"Role: {role_title}\n"
            "Task: You are surgically refining the previous output based on direct user feedback. "
            "Strictly incorporate the user's feedback into the output while maintaining clean, structured formatting. "
            "Preserve all existing valid data while applying the requested revisions."
        )
        refinement_user_prompt = f"Original Output:\n{original_output}\n\nUser Feedback:\n{user_feedback}"
        yield from self.stream(refinement_system_prompt, refinement_user_prompt)

    def get_status(self) -> dict:
        """Returns health and runtime status of the LLM connection."""
        return {
            "active_model": self.active_model_name,
            "base_url": self.config.ollama_base_url,
            "num_gpu": self.config.ollama_num_gpu,
            "num_ctx": self.config.ollama_num_ctx,
            "temperature": self.config.temperature
        }

_instance: Optional[LLMService] = None

def get_llm_service(config: Optional[AppConfig] = None) -> LLMService:
    """Returns singleton LLMService instance."""
    global _instance
    if _instance is None:
        _instance = LLMService(config)
    return _instance

from abc import ABC, abstractmethod
from typing import Optional, Generator
from ..core.llm_service import LLMService, get_llm_service

class BaseStage(ABC):
    """Abstract base class for all pipeline stages."""
    
    def __init__(self, stage_number: int, stage_name: str, llm_service: Optional[LLMService] = None):
        self.stage_number = stage_number
        self.stage_name = stage_name
        self.llm = llm_service or get_llm_service()

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Returns the system prompt defining the stage persona and instructions."""
        pass

    def execute(self, input_data: str) -> str:
        """Executes the initial prompt for this stage synchronously."""
        return self.llm.invoke(self.system_prompt, f"Input Data / Context:\n{input_data}")

    def execute_stream(self, input_data: str) -> Generator[str, None, None]:
        """Streams the initial prompt execution tokens in real-time."""
        yield from self.llm.stream(self.system_prompt, f"Input Data / Context:\n{input_data}")

    def refine(self, current_output: str, feedback: str) -> str:
        """Refines the current output based on user feedback synchronously."""
        return self.llm.refine(current_output, feedback, role_title=f"Agile Specialist ({self.stage_name})")

    def refine_stream(self, current_output: str, feedback: str) -> Generator[str, None, None]:
        """Streams refined output tokens in real-time."""
        yield from self.llm.stream_refine(current_output, feedback, role_title=f"Agile Specialist ({self.stage_name})")

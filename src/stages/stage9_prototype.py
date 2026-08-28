from typing import List
from pathlib import Path
from .base_stage import BaseStage
from ..prompts.agile_prompts import PROMPT_STAGE_9_TECH_STACK, PROMPT_STAGE_9_PROTOTYPE
from ..utils.file_extractor import extract_and_save_code_files

class Stage9Prototype(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(9, "Tech Stack & Executable Prototype Generation", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_9_PROTOTYPE

    def recommend_tech_stack(self, sprint_context: str) -> str:
        """Executes Sub-stage 9A: Tech stack recommendation."""
        return self.llm.invoke(PROMPT_STAGE_9_TECH_STACK, f"Selected Sprint Stories:\n{sprint_context}")

    def negotiate_tech_stack(self, previous_discussion: str, developer_input: str) -> str:
        """Conducts Sub-stage 9A: Architect-Developer negotiation."""
        negotiation_system_prompt = (
            "Role: Principal Software Architect\n"
            "Task: Discuss the tech stack choice with the developer. Address their questions, analyze trade-offs of their proposed stack versus the recommended one, "
            "and finalize the agreed tech stack architecture for the prototype."
        )
        negotiation_user_prompt = f"Previous Discussion:\n{previous_discussion}\n\nDeveloper Feedback:\n{developer_input}"
        return self.llm.invoke(negotiation_system_prompt, negotiation_user_prompt)

    def generate_code(self, sprint_context: str, tech_stack_agreement: str) -> str:
        """Executes Sub-stage 9B: Generates complete executable prototype code."""
        prompt_input = f"Approved Sprint Context:\n{sprint_context}\n\nAgreed Tech Stack Architecture:\n{tech_stack_agreement}"
        return self.llm.invoke(PROMPT_STAGE_9_PROTOTYPE, prompt_input)

    def extract_and_save(self, code_output: str, target_dir: Path) -> List[Path]:
        """Saves generated code files directly to disk."""
        return extract_and_save_code_files(code_output, target_dir)

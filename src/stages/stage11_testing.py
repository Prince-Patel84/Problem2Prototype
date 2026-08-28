from pathlib import Path
from typing import List, Tuple
from .base_stage import BaseStage
from ..prompts.agile_prompts import PROMPT_STAGE_11_AUTO_HEAL
from ..utils.pytest_runner import execute_pytest_suite, PytestResult
from ..utils.file_extractor import extract_and_save_code_files

class Stage11Testing(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(11, "Automated Testing & AI Auto-Healing", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_11_AUTO_HEAL

    def run_tests(self, prototype_dir: Path) -> PytestResult:
        """Runs pytest across all test files in the prototype directory."""
        return execute_pytest_suite(prototype_dir, working_dir=prototype_dir)

    def auto_heal(self, pytest_output: str, user_instructions: str, prototype_dir: Path) -> Tuple[str, List[Path]]:
        """Reads all code and test files, invokes healing LLM, and updates files on disk."""
        code_context = ""
        for pfile in prototype_dir.glob("*.py"):
            with open(pfile, "r", encoding="utf-8") as f:
                code_context += f"\n--- Current {pfile.name} ---\n```python\n# filename: {pfile.name}\n" + f.read() + "\n```\n"

        user_content = f"Pytest Failure Output:\n{pytest_output}\n\nUser Instructions / Feedback:\n{user_instructions}\n\nCurrent Code & Test Files:\n{code_context}"
        repaired_content = self.llm.invoke(self.system_prompt, user_content)
        saved_files = extract_and_save_code_files(repaired_content, prototype_dir)
        return repaired_content, saved_files

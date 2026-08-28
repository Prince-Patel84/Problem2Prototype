from pathlib import Path
from typing import List, Generator
from .base_stage import BaseStage
from ..prompts.agile_prompts import PROMPT_STAGE_10_TEST_CASES
from ..utils.file_extractor import extract_and_save_code_files

class Stage10TestCases(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(10, "Test Case & Pytest Suite Generation", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_10_TEST_CASES

    def generate_tests(self, sprint_stories: str, prototype_code: str) -> str:
        """Generates test cases and pytest script synchronously."""
        prompt_input = f"Selected Sprint Stories:\n{sprint_stories}\n\nGenerated Prototype Implementation:\n{prototype_code}"
        return self.llm.invoke(self.system_prompt, prompt_input)

    def generate_tests_stream(self, sprint_stories: str, prototype_code: str) -> Generator[str, None, None]:
        """Streams test cases and pytest script generation in real-time."""
        prompt_input = f"Selected Sprint Stories:\n{sprint_stories}\n\nGenerated Prototype Implementation:\n{prototype_code}"
        yield from self.llm.stream(self.system_prompt, prompt_input)

    def extract_and_save(self, test_output: str, target_dir: Path) -> List[Path]:
        return extract_and_save_code_files(test_output, target_dir)

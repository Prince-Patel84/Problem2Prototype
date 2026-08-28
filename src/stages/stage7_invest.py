from .base_stage import BaseStage
from ..prompts.agile_prompts import PROMPT_STAGE_7_INVEST

class Stage7Invest(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(7, "INVEST Criteria Check & Quality Gate", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_7_INVEST

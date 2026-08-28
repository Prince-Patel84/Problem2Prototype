from .base_stage import BaseStage
from ..prompts.elicitation_prompts import PROMPT_STAGE_2_GOALS

class Stage2Goals(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(2, "Stakeholder Goals & Needs Analysis", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_2_GOALS

from .base_stage import BaseStage
from ..prompts.agile_prompts import PROMPT_STAGE_8_SPRINTS

class Stage8Sprints(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(8, "Sprint Grouping & Estimation", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_8_SPRINTS

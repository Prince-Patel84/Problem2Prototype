from .base_stage import BaseStage
from ..prompts.elicitation_prompts import PROMPT_STAGE_1_STAKEHOLDERS

class Stage1Stakeholders(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(1, "Stakeholder Identification", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_1_STAKEHOLDERS

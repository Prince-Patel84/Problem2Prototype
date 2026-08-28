from .base_stage import BaseStage
from ..prompts.elicitation_prompts import PROMPT_STAGE_4_ELICITATION

class Stage4Elicitation(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(4, "Elicitation Execution", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_4_ELICITATION

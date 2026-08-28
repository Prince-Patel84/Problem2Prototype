from .base_stage import BaseStage
from ..prompts.elicitation_prompts import PROMPT_STAGE_3_SELECTION

class Stage3Selection(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(3, "Elicitation Technique Selection", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_3_SELECTION

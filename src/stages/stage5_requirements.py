from .base_stage import BaseStage
from ..prompts.elicitation_prompts import PROMPT_STAGE_5_REQUIREMENTS

class Stage5Requirements(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(5, "FR & NFR Generation", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_5_REQUIREMENTS

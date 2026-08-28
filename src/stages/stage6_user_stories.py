from .base_stage import BaseStage
from ..prompts.agile_prompts import PROMPT_STAGE_6_USER_STORIES

class Stage6UserStories(BaseStage):
    def __init__(self, llm_service=None):
        super().__init__(6, "User Story Generation (Agile Cards)", llm_service)

    @property
    def system_prompt(self) -> str:
        return PROMPT_STAGE_6_USER_STORIES

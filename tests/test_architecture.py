import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.config import get_config, AppConfig
from src.utils.file_extractor import extract_and_save_code_files
from src.utils.pytest_runner import execute_pytest_suite, PytestResult
from src.prompts import (
    PROMPT_STAGE_1_STAKEHOLDERS,
    PROMPT_STAGE_6_USER_STORIES,
    PROMPT_STAGE_9_PROTOTYPE,
    PROMPT_STAGE_11_AUTO_HEAL,
)
from src.stages import (
    BaseStage,
    Stage1Stakeholders,
    Stage2Goals,
    Stage3Selection,
    Stage4Elicitation,
    Stage5Requirements,
    Stage6UserStories,
    Stage7Invest,
    Stage8Sprints,
    Stage9Prototype,
    Stage10TestCases,
    Stage11Testing,
)

def test_config_initialization():
    config = get_config()
    assert isinstance(config, AppConfig)
    assert config.ollama_num_gpu == 99
    assert config.ollama_num_ctx == 2048
    assert config.artifacts_dir.exists()
    assert config.prototype_dir.exists()

def test_prompt_registry_completeness():
    assert len(PROMPT_STAGE_1_STAKEHOLDERS) > 50
    assert len(PROMPT_STAGE_6_USER_STORIES) > 50
    assert len(PROMPT_STAGE_9_PROTOTYPE) > 50
    assert len(PROMPT_STAGE_11_AUTO_HEAL) > 50

def test_stages_instantiation():
    # Pass a dummy llm_service to test stage instantiation without making network calls
    class DummyLLM:
        pass
    dummy = DummyLLM()
    
    stages = [
        Stage1Stakeholders(dummy),
        Stage2Goals(dummy),
        Stage3Selection(dummy),
        Stage4Elicitation(dummy),
        Stage5Requirements(dummy),
        Stage6UserStories(dummy),
        Stage7Invest(dummy),
        Stage8Sprints(dummy),
        Stage9Prototype(dummy),
        Stage10TestCases(dummy),
        Stage11Testing(dummy),
    ]
    
    for idx, stage in enumerate(stages, start=1):
        assert isinstance(stage, BaseStage)
        assert stage.stage_number == idx
        assert len(stage.system_prompt) > 20

def test_file_extractor(tmp_path):
    sample_llm_code = """
Here is the code:
```python
# filename: dummy_engine.py
def add(a, b):
    return a + b
```
```python
# filename: dummy_app.py
import streamlit as st
st.title('Test App')
```
"""
    saved_files = extract_and_save_code_files(sample_llm_code, tmp_path)
    assert len(saved_files) == 2
    f1 = tmp_path / "dummy_engine.py"
    f2 = tmp_path / "dummy_app.py"
    assert f1.exists()
    assert f2.exists()
    assert "def add(a, b):" in f1.read_text(encoding="utf-8")
    assert "st.title('Test App')" in f2.read_text(encoding="utf-8")

def test_pytest_runner_on_valid_prototype():
    prototype_dir = Path(__file__).resolve().parent.parent / "prototype"
    test_file = prototype_dir / "test_prototype.py"
    if test_file.exists():
        result = execute_pytest_suite(test_file, working_dir=prototype_dir)
        assert isinstance(result, PytestResult)
        assert result.passed is True
        assert result.failed_tests == 0
        assert result.passed_tests > 0

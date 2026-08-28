import pytest
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.stages.base_stage import BaseStage
from src.stages.stage1_stakeholders import Stage1Stakeholders

def test_base_stage_streaming_interface():
    class MockStreamingLLM:
        def stream(self, system_prompt, user_content):
            chunks = ["Hello", " ", "world", "!"]
            for chunk in chunks:
                yield chunk
                
        def stream_refine(self, original_output, user_feedback, role_title=""):
            chunks = ["Refined", " ", "output", "!"]
            for chunk in chunks:
                yield chunk

    mock_llm = MockStreamingLLM()
    stage = Stage1Stakeholders(mock_llm)
    
    # Test execute_stream
    stream_gen = stage.execute_stream("Input text")
    collected = "".join(list(stream_gen))
    assert collected == "Hello world!"
    
    # Test refine_stream
    refine_gen = stage.refine_stream("Initial", "Feedback")
    collected_refine = "".join(list(refine_gen))
    assert collected_refine == "Refined output!"

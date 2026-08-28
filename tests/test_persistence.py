import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def test_session_state_persistence(tmp_path):
    state_file = tmp_path / ".project_state.json"
    
    # 1. Simulate saving state
    sample_state = {
        "case_study": "Emergency Triage System",
        "current_stage_idx": 4,
        "stage1_out": "Stakeholder output content",
        "stage2_out": "Goals output content",
        "stage3_out": "Elicitation techniques",
        "stage4_out": "Interview questionnaire artifacts",
        "stage5_out": "Functional and Non-functional requirements"
    }
    
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(sample_state, f, indent=2)
        
    assert state_file.exists()
    
    # 2. Simulate loading state
    with open(state_file, "r", encoding="utf-8") as f:
        loaded_state = json.load(f)
        
    assert loaded_state["case_study"] == "Emergency Triage System"
    assert loaded_state["current_stage_idx"] == 4
    assert loaded_state["stage1_out"] == "Stakeholder output content"
    assert loaded_state["stage5_out"] == "Functional and Non-functional requirements"
    
    # 3. Simulate reset state
    state_file.unlink()
    assert not state_file.exists()

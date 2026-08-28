import os
import sys
import io
import zipfile
from pathlib import Path
import streamlit as st

# Add workspace to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.config import get_config
from src.core.llm_service import get_llm_service
from src.stages import (
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

# Initialize App Configuration
config = get_config()

# Page Setup
st.set_page_config(
    page_title="Problem2Prototype Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------------------------------------
DEFAULT_CASE_STUDY = """LIC, an insurance company, wants to digitize a range of business processes and provide a complete solution that addresses all aspects of the agent-insurer relationship. 
The first product LIC wants you to develop is a system for creating consolidated insurance packages that can compete with packages provided by other insurance companies. 
Another product is based on customer priority. Based on the insurance policies available, the customer can create his/her own package by selecting suitable policies and send a request for review. The system has to automatically analyze the proposed package, identify possible issues or restrictions, provide suggestions, and finally give a competing price."""

if "case_study" not in st.session_state:
    st.session_state.case_study = DEFAULT_CASE_STUDY

STAGE_KEYS = [
    "stage1_out", "stage2_out", "stage3_out", "stage4_out", "stage5_out",
    "stage6_out", "stage7_out", "stage8_out", "stage9a_out", "stage9b_out",
    "stage10_out", "stage11_out"
]

for key in STAGE_KEYS:
    if key not in st.session_state:
        st.session_state[key] = ""

if "current_stage_idx" not in st.session_state:
    st.session_state.current_stage_idx = 0

if "test_results" not in st.session_state:
    st.session_state.test_results = None

# Auto-load existing Output.txt if available and stage 5 is empty
output_file = config.base_dir / "Output.txt"
if output_file.exists() and not st.session_state.stage5_out:
    try:
        st.session_state.stage5_out = output_file.read_text(encoding="utf-8")
    except Exception:
        pass

# Initialize LLM Service (Cached Resource)
@st.cache_resource
def load_llm():
    return get_llm_service(config)

try:
    llm = load_llm()
    llm_status = llm.get_status()
    llm_ok = True
except Exception as e:
    llm_status = {"active_model": "None", "error": str(e)}
    llm_ok = False

# ------------------------------------------------------------------------------
# SIDEBAR NAVIGATION & STATUS
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("⚡ Problem2Prototype")
    st.caption("Autonomous Requirements to Executable Prototype Studio")
    
    with st.container(border=True):
        st.markdown("**Local LLM Engine**")
        if llm_ok:
            st.success(f"🤖 `{llm_status['active_model']}` (100% GPU)", icon=":material/check_circle:")
        else:
            st.error("Ollama connection failed", icon=":material/error:")
            
    st.divider()
    st.subheader("Pipeline Stages")
    
    stages_metadata = [
        ("1. Stakeholders", ":material/group:"),
        ("2. Goals Analysis", ":material/flag:"),
        ("3. Elicitation Tech", ":material/psychology:"),
        ("4. Elicitation Run", ":material/quiz:"),
        ("5. FR & NFR Specs", ":material/assignment:"),
        ("6. Agile User Stories", ":material/view_kanban:"),
        ("7. INVEST Quality Gate", ":material/verified:"),
        ("8. Sprint Planning", ":material/schedule:"),
        ("9. Tech Stack & Prototype", ":material/code:"),
        ("10. Test Case Generation", ":material/bug_report:"),
        ("11. Automated Testing Lab", ":material/play_circle:"),
    ]

    for idx, (label, icon) in enumerate(stages_metadata):
        state_key = STAGE_KEYS[idx if idx < 9 else (9 if idx == 8 else (10 if idx == 9 else 11))]
        is_completed = bool(st.session_state.get(state_key, ""))
        
        btn_label = f"{label} {'✅' if is_completed else ''}"
        btn_type = "primary" if st.session_state.current_stage_idx == idx else "secondary"
        
        if st.button(btn_label, key=f"nav_btn_{idx}", type=btn_type, icon=icon, use_container_width=True):
            st.session_state.current_stage_idx = idx
            st.rerun()

    st.divider()
    st.subheader("Deliverables Export")
    
    # Create zip export in-memory
    def generate_zip_bundle():
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in config.artifacts_dir.glob("*.*"):
                zf.write(p, arcname=f"artifacts/{p.name}")
            for p in config.prototype_dir.glob("*.*"):
                zf.write(p, arcname=f"prototype/{p.name}")
            report_p = config.base_dir / "Report.md"
            if report_p.exists():
                zf.write(report_p, arcname="Report.md")
        buf.seek(0)
        return buf

    st.download_button(
        label="Download Project Zip Bundle",
        data=generate_zip_bundle(),
        file_name="Lab4_Agile_Requirements_Package.zip",
        mime="application/zip",
        icon=":material/download:",
        use_container_width=True
    )

# ------------------------------------------------------------------------------
# STAGE EXECUTION RENDERERS
# ------------------------------------------------------------------------------

current_idx = st.session_state.current_stage_idx

def render_hitl_stage(title: str, stage_obj, state_key: str, input_data: str, placeholder_text: str = ""):
    st.header(title)
    
    col_out, col_hitl = st.columns([1.2, 0.8])
    
    with col_out:
        with st.container(border=True):
            st.subheader("Generated Stage Output")
            current_val = st.session_state.get(state_key, "")
            
            if not current_val:
                st.info(f"Click **Execute {title}** to generate output using local AI.", icon=":material/info:")
                if st.button(f"Generate {title}", type="primary", icon=":material/play_arrow:"):
                    with st.spinner("Processing with Hermes 3 on GPU..."):
                        res = stage_obj.execute(input_data)
                        st.session_state[state_key] = res
                        st.rerun()
            else:
                st.markdown(current_val)
                with st.expander("Edit Raw Markdown Directly", expanded=False):
                    edited_text = st.text_area("Direct Editor", value=current_val, height=300, label_visibility="collapsed")
                    if st.button("Save Manual Edits", key=f"save_edit_{state_key}", icon=":material/save:"):
                        st.session_state[state_key] = edited_text
                        st.success("Manual edits saved!", icon=":material/check:")
                        st.rerun()

    with col_hitl:
        with st.container(border=True):
            st.subheader("Human-In-The-Loop Steering")
            st.markdown("Provide feedback to steer the output or approve to move to the next stage.")
            
            feedback = st.text_area(
                "Feedback / Correction Prompt",
                placeholder="e.g., Add policy administrators, include critical illness rider constraints, or adjust story points...",
                height=140,
                key=f"feedback_{state_key}"
            )
            
            bcol1, bcol2 = st.columns(2)
            with bcol1:
                if st.button("Refine Output", key=f"refine_{state_key}", icon=":material/auto_fix_high:", use_container_width=True):
                    if feedback.strip() and st.session_state.get(state_key):
                        with st.spinner("Surgically refining output..."):
                            refined = stage_obj.refine(st.session_state[state_key], feedback)
                            st.session_state[state_key] = refined
                            st.rerun()
                    else:
                        st.warning("Please enter feedback before refining.")
            
            with bcol2:
                if st.button("Approve & Next ➔", key=f"approve_{state_key}", type="primary", icon=":material/arrow_forward:", use_container_width=True):
                    st.session_state.current_stage_idx = min(10, current_idx + 1)
                    st.rerun()

# ------------------------------------------------------------------------------
# MAIN WORKSPACE ROUTING
# ------------------------------------------------------------------------------

# Case Study & Context Bar
with st.expander("📝 Target System / Case Study Specification", expanded=(current_idx == 0 and not st.session_state.stage1_out)):
    case_in = st.text_area("Problem Statement", value=st.session_state.case_study, height=120)
    if st.button("Update Case Study Context", icon=":material/sync:"):
        st.session_state.case_study = case_in
        st.success("Updated active case study!")

# Stage 1: Stakeholders
if current_idx == 0:
    s1 = Stage1Stakeholders(llm)
    render_hitl_stage("Stage 1: Stakeholder Identification", s1, "stage1_out", st.session_state.case_study)

# Stage 2: Goals
elif current_idx == 1:
    s2 = Stage2Goals(llm)
    in_data = st.session_state.stage1_out or st.session_state.case_study
    render_hitl_stage("Stage 2: Stakeholder Goals & Needs Analysis", s2, "stage2_out", in_data)

# Stage 3: Elicitation Technique Selection
elif current_idx == 2:
    s3 = Stage3Selection(llm)
    in_data = st.session_state.stage2_out or st.session_state.case_study
    render_hitl_stage("Stage 3: Elicitation Technique Selection", s3, "stage3_out", in_data)

# Stage 4: Elicitation Execution
elif current_idx == 3:
    s4 = Stage4Elicitation(llm)
    in_data = st.session_state.stage3_out or st.session_state.case_study
    render_hitl_stage("Stage 4: Elicitation Artifacts Execution", s4, "stage4_out", in_data)

# Stage 5: FR & NFR Specs
elif current_idx == 4:
    s5 = Stage5Requirements(llm)
    in_data = st.session_state.stage4_out or st.session_state.case_study
    render_hitl_stage("Stage 5: Functional & Non-Functional Requirements", s5, "stage5_out", in_data)
    if st.session_state.stage5_out:
        with open(config.base_dir / "Output.txt", "w", encoding="utf-8") as f:
            f.write(st.session_state.stage5_out)

# Stage 6: Agile User Stories
elif current_idx == 5:
    s6 = Stage6UserStories(llm)
    in_data = st.session_state.stage5_out or st.session_state.case_study
    render_hitl_stage("Stage 6: Agile User Story Generation (Agile Cards)", s6, "stage6_out", in_data)
    if st.session_state.stage6_out:
        with open(config.artifacts_dir / "user_stories.md", "w", encoding="utf-8") as f:
            f.write("# Generated Agile User Stories\n\n" + st.session_state.stage6_out)

# Stage 7: INVEST Quality Gate
elif current_idx == 6:
    s7 = Stage7Invest(llm)
    in_data = st.session_state.stage6_out or st.session_state.stage5_out
    render_hitl_stage("Stage 7: INVEST Criteria Check & Quality Audit", s7, "stage7_out", in_data)
    if st.session_state.stage7_out:
        with open(config.artifacts_dir / "invest_evaluation.md", "w", encoding="utf-8") as f:
            f.write("# INVEST Quality Evaluation Report\n\n" + st.session_state.stage7_out)

# Stage 8: Sprint Planning
elif current_idx == 7:
    s8 = Stage8Sprints(llm)
    in_data = st.session_state.stage7_out or st.session_state.stage6_out
    render_hitl_stage("Stage 8: Sprint Grouping & Estimation", s8, "stage8_out", in_data)
    if st.session_state.stage8_out:
        with open(config.artifacts_dir / "sprint_plan.md", "w", encoding="utf-8") as f:
            f.write("# Sprint Planning & Groupings\n\n" + st.session_state.stage8_out)

# Stage 9: Tech Stack Negotiation & Prototype Generation
elif current_idx == 8:
    st.header("Stage 9: Tech Stack Negotiation & Executable Prototyping")
    s9 = Stage9Prototype(llm)
    sprint_in = st.session_state.stage8_out or st.session_state.stage6_out
    
    t1, t2 = st.tabs(["9A: Tech Stack Discussion & Negotiation", "9B: Generated Prototype Code"])
    
    with t1:
        st.subheader("Architect Recommendation & Negotiation")
        if not st.session_state.stage9a_out:
            if st.button("Generate Tech Stack Proposal", type="primary", icon=":material/architecture:"):
                with st.spinner("Analyzing sprint stories and evaluating trade-offs..."):
                    st.session_state.stage9a_out = s9.recommend_tech_stack(sprint_in)
                    st.rerun()
        else:
            st.markdown(st.session_state.stage9a_out)
            dev_feedback = st.text_input("Developer Suggestion / Alternative Stack Preference", placeholder="e.g., Recommend Streamlit for speed, or negotiate Flask/React...")
            if st.button("Send to Architect for Review", icon=":material/send:"):
                with st.spinner("Architect analyzing trade-offs..."):
                    st.session_state.stage9a_out = s9.negotiate_tech_stack(st.session_state.stage9a_out, dev_feedback)
                    st.rerun()

    with t2:
        st.subheader("Executable Prototype Code Generation")
        if not st.session_state.stage9b_out:
            if st.button("Generate Executable Prototype Code", type="primary", icon=":material/code:"):
                with st.spinner("Generating modular Python engine and Streamlit application..."):
                    code_res = s9.generate_code(sprint_in, st.session_state.stage9a_out)
                    st.session_state.stage9b_out = code_res
                    saved_files = s9.extract_and_save(code_res, config.prototype_dir)
                    st.rerun()
        else:
            st.markdown(st.session_state.stage9b_out)
            
            with st.container(border=True):
                st.subheader("Files on Disk (`prototype/`)")
                for pfile in config.prototype_dir.glob("*.py"):
                    st.write(f"- `{pfile.name}` ({pfile.stat().st_size} bytes)")
                
                st.info("To run this prototype in a separate window: `.venv\\Scripts\\streamlit run prototype/prototype_app.py`", icon=":material/terminal:")
                if st.button("Approve Prototype Code & Proceed to Tests ➔", type="primary", icon=":material/arrow_forward:"):
                    st.session_state.current_stage_idx = 9
                    st.rerun()

# Stage 10: Test Case Generation
elif current_idx == 9:
    s10 = Stage10TestCases(llm)
    sprint_in = st.session_state.stage8_out or st.session_state.stage6_out
    proto_in = st.session_state.stage9b_out or ""
    
    st.header("Stage 10: Test Case & Pytest Suite Generation")
    
    if not st.session_state.stage10_out:
        if st.button("Generate Test Cases & Pytest Script", type="primary", icon=":material/bug_report:"):
            with st.spinner("Generating structured test cases and pytest suite..."):
                test_res = s10.generate_tests(sprint_in, proto_in)
                st.session_state.stage10_out = test_res
                s10.extract_and_save(test_res, config.prototype_dir)
                with open(config.artifacts_dir / "test_specifications.md", "w", encoding="utf-8") as f:
                    f.write("# Generated Test Specifications\n\n" + test_res)
                st.rerun()
    else:
        st.markdown(st.session_state.stage10_out)
        if st.button("Approve Test Suite & Enter Automated Testing Lab ➔", type="primary", icon=":material/arrow_forward:"):
            st.session_state.current_stage_idx = 10
            st.rerun()

# Stage 11: Automated Testing Lab & Auto-Healing
elif current_idx == 10:
    st.header("Stage 11: Automated Testing Lab & AI Auto-Healing")
    s11 = Stage11Testing(llm)
    
    with st.container(border=True):
        st.subheader("Pytest Execution Runner")
        rcol1, rcol2 = st.columns([1, 1])
        with rcol1:
            if st.button("Run Automated Pytest Suite", type="primary", icon=":material/play_circle:", use_container_width=True):
                with st.spinner("Executing pytest against prototype in virtual environment..."):
                    res = s11.run_tests(config.prototype_dir)
                    st.session_state.test_results = res
                    st.session_state.stage11_out = res.output
                    with open(config.artifacts_dir / "test_results.md", "w", encoding="utf-8") as f:
                        f.write(f"# Automated Test Execution Results\n\n```\n{res.output}\n```\n")
                    st.rerun()

        res_obj = st.session_state.test_results
        if res_obj:
            if res_obj.passed:
                st.success(f"🎉 ALL TESTS PASSED! ({res_obj.passed_tests}/{res_obj.total_tests} Tests Passed)", icon=":material/check_circle:")
            else:
                st.error(f"❌ TEST FAILURES DETECTED ({res_obj.failed_tests} Failed, {res_obj.passed_tests} Passed)", icon=":material/cancel:")
                
            st.code(res_obj.output, language="text")
            
            # AI Auto-Healing Section
            if not res_obj.passed:
                with st.container(border=True):
                    st.subheader("🛠️ AI Auto-Healing & Code Repair")
                    st.markdown("Instruct the AI on how to repair the failing tests or trigger automated code diagnosis.")
                    heal_instr = st.text_input("Custom Repair Instructions (Optional)", placeholder="e.g. Fix formula calculation in insurance_engine.py")
                    if st.button("Trigger AI Auto-Healing", type="primary", icon=":material/healing:"):
                        with st.spinner("AI analyzing test traceback and repairing code..."):
                            rep_code, updated_files = s11.auto_heal(res_obj.output, heal_instr or "auto", config.prototype_dir)
                            st.success(f"Updated code on disk: {[f.name for f in updated_files]}")
                            # Auto re-run pytest
                            new_res = s11.run_tests(config.prototype_dir)
                            st.session_state.test_results = new_res
                            st.session_state.stage11_out = new_res.output
                            st.rerun()

import os
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
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

def run_cli_stage(stage_obj, input_data: str, auto_approve: bool = False) -> str:
    """Executes a stage via CLI with interactive HITL review."""
    print("\n" + "="*70)
    print(f"  EXECUTING STAGE {stage_obj.stage_number}: {stage_obj.stage_name.upper()}")
    print("="*70)

    current_output = stage_obj.execute(input_data)
    
    while True:
        print(f"\n" + "-"*25 + f" [ Output: {stage_obj.stage_name} ] " + "-"*25 + "\n")
        print(current_output)
        print("\n" + "-"*70)

        if auto_approve:
            print("[+] Auto-approve flag set. Proceeding...")
            return current_output

        feedback = input(f"\n[HITL Review] Enter edits/feedback for Stage {stage_obj.stage_number} (or 'approve' to proceed): ").strip()
        
        if feedback.lower() == 'approve':
            print(f"[+] Stage {stage_obj.stage_number} Approved. Proceeding to next stage...\n")
            return current_output
        elif not feedback:
            continue
            
        print(f"[*] Refining output with user feedback...")
        current_output = stage_obj.refine(current_output, feedback)

def main():
    parser = argparse.ArgumentParser(description="Agile Requirements Engineering & Prototyping Pipeline CLI")
    parser.add_argument("--input", "-i", type=str, help="Path to input case study file or text description")
    parser.add_argument("--auto", action="store_true", help="Auto-approve intermediate stages without interactive prompts")
    args = parser.parse_args()

    config = get_config()
    llm = get_llm_service(config)

    print("\n" + "#"*70)
    print("  AGILE REQUIREMENTS ENGINEERING & EXECUTABLE PROTOTYPING STUDIO")
    print(f"  Local Model Engine: {llm.active_model_name} [100% GPU Offload]")
    print("#"*70)

    # 1. Determine Input
    final_fr_nfr = ""
    case_input = ""

    if args.input:
        in_path = Path(args.input)
        if in_path.exists() and in_path.is_file():
            case_input = in_path.read_text(encoding="utf-8")
        else:
            case_input = args.input
    else:
        output_file = config.base_dir / "Output.txt"
        if output_file.exists():
            print(f"\n[?] Found existing 'Output.txt' (FR/NFR specification).")
            choice = input("    Use 'Output.txt' directly for Stage 6? (Y/n, or enter new description/path): ").strip()
            if choice.lower() in ["", "y", "yes"]:
                final_fr_nfr = output_file.read_text(encoding="utf-8")
            elif Path(choice).exists() and Path(choice).is_file():
                case_input = Path(choice).read_text(encoding="utf-8")
            elif len(choice) > 10:
                case_input = choice
            else:
                case_input = input("\nEnter system description: ").strip()
        else:
            print("\nEnter system description or path to text file (Press Enter for default LIC Case Study):")
            user_in = input("> ").strip()
            if Path(user_in).exists() and Path(user_in).is_file():
                case_input = Path(user_in).read_text(encoding="utf-8")
            elif user_in:
                case_input = user_in
            else:
                case_input = """LIC, an insurance company, wants to digitize a range of business processes and provide a complete solution that addresses all aspects of the agent-insurer relationship. 
The first product LIC wants you to develop is a system for creating consolidated insurance packages that can compete with packages provided by other insurance companies. 
Another product is based on customer priority. Based on the insurance policies available, the customer can create his/her own package by selecting suitable policies and send a request for review. The system has to automatically analyze the proposed package, identify possible issues or restrictions, provide suggestions, and finally give a competing price."""

    # 2. Execute Stages 1 to 5 (if needed)
    if not final_fr_nfr:
        s1 = Stage1Stakeholders(llm)
        out1 = run_cli_stage(s1, case_input, args.auto)
        
        s2 = Stage2Goals(llm)
        out2 = run_cli_stage(s2, out1, args.auto)
        
        s3 = Stage3Selection(llm)
        out3 = run_cli_stage(s3, out2, args.auto)
        
        s4 = Stage4Elicitation(llm)
        out4 = run_cli_stage(s4, out3, args.auto)
        
        s5 = Stage5Requirements(llm)
        final_fr_nfr = run_cli_stage(s5, out4, args.auto)
        
        with open(config.base_dir / "Output.txt", "w", encoding="utf-8") as f:
            f.write(final_fr_nfr)

    # 3. Stage 6: Agile User Stories
    s6 = Stage6UserStories(llm)
    out6 = run_cli_stage(s6, final_fr_nfr, args.auto)
    with open(config.artifacts_dir / "user_stories.md", "w", encoding="utf-8") as f:
        f.write("# Generated Agile User Stories\n\n" + out6)

    # 4. Stage 7: INVEST Quality Audit
    s7 = Stage7Invest(llm)
    out7 = run_cli_stage(s7, out6, args.auto)
    with open(config.artifacts_dir / "invest_evaluation.md", "w", encoding="utf-8") as f:
        f.write("# INVEST Quality Evaluation Report\n\n" + out7)

    # 5. Stage 8: Sprint Planning
    s8 = Stage8Sprints(llm)
    out8 = run_cli_stage(s8, out7, args.auto)
    with open(config.artifacts_dir / "sprint_plan.md", "w", encoding="utf-8") as f:
        f.write("# Sprint Plan\n\n" + out8)

    # 6. Stage 9: Tech Stack Negotiation & Prototype Generation
    s9 = Stage9Prototype(llm)
    print("\n" + "="*70)
    print("  STAGE 9A: TECH STACK RECOMMENDATION & NEGOTIATION")
    print("="*70)
    stack_prop = s9.recommend_tech_stack(out8)
    print(stack_prop)
    
    if not args.auto:
        dev_in = input("\n[Developer Input] Enter preferences, or type 'approve' to proceed with proposed stack: ").strip()
        if dev_in.lower() != 'approve' and dev_in:
            stack_prop = s9.negotiate_tech_stack(stack_prop, dev_in)
            print("\n--- Updated Tech Stack Agreement ---\n" + stack_prop)

    print("\n" + "="*70)
    print("  STAGE 9B: EXECUTABLE PROTOTYPE CODE GENERATION")
    print("="*70)
    proto_code = s9.generate_code(out8, stack_prop)
    saved_proto_files = s9.extract_and_save(proto_code, config.prototype_dir)
    print(f"[+] Saved prototype files: {[f.name for f in saved_proto_files]}")

    # 7. Stage 10: Test Case Generation
    s10 = Stage10TestCases(llm)
    print("\n" + "="*70)
    print("  STAGE 10: TEST CASE & PYTEST SUITE GENERATION")
    print("="*70)
    test_specs = s10.generate_tests(out8, proto_code)
    s10.extract_and_save(test_specs, config.prototype_dir)
    with open(config.artifacts_dir / "test_specifications.md", "w", encoding="utf-8") as f:
        f.write("# Generated Test Specifications\n\n" + test_specs)

    # 8. Stage 11: Automated Testing Lab & Auto-Healing
    s11 = Stage11Testing(llm)
    print("\n" + "="*70)
    print("  STAGE 11: AUTOMATED TESTING LAB & AI AUTO-HEALING")
    print("="*70)
    
    while True:
        res = s11.run_tests(config.prototype_dir)
        print("\n--- Pytest Output ---")
        print(res.output)
        
        if res.passed:
            print("\n[+] ALL TESTS PASSED (100% Pass Rate)!")
            break
        else:
            print(f"\n[!] {res.failed_tests} Tests Failed.")
            if args.auto:
                print("[*] Triggering automated AI code healing...")
                s11.auto_heal(res.output, "auto", config.prototype_dir)
            else:
                user_heal = input("\nEnter repair instruction (or 'auto' for AI auto-repair, 'approve' to exit): ").strip()
                if user_heal.lower() == 'approve':
                    break
                s11.auto_heal(res.output, user_heal or "auto", config.prototype_dir)

    with open(config.artifacts_dir / "test_results.md", "w", encoding="utf-8") as f:
        f.write(f"# Automated Test Execution Results\n\n```\n{res.output}\n```\n")

    print("\n" + "="*70)
    print("  PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"  Artifacts directory: {config.artifacts_dir}")
    print(f"  Prototype directory: {config.prototype_dir}")
    print("  Launch Web Studio: .venv\\Scripts\\streamlit run app.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
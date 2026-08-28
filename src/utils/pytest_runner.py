import os
import sys
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class PytestResult:
    """Encapsulates the execution result of an automated pytest run."""
    passed: bool
    return_code: int
    output: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0

def execute_pytest_suite(test_file: Union[str, Path], working_dir: Optional[Union[str, Path]] = None) -> PytestResult:
    """
    Programmatically executes pytest against a specified test file in a subprocess,
    ensuring proper virtual environment python and PYTHONPATH resolution.
    """
    test_path = Path(test_file).resolve()
    base_dir = Path(working_dir).resolve() if working_dir else test_path.parent
    
    venv_python = sys.executable
    
    env = os.environ.copy()
    # Ensure working_dir is in PYTHONPATH so local imports work deterministically
    env["PYTHONPATH"] = str(base_dir) + os.pathsep + env.get("PYTHONPATH", "")
    
    cmd = [venv_python, "-m", "pytest", str(test_path), "-v", "--tb=short"]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
        output = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
        passed = (proc.returncode == 0)
        
        # Simple extraction of counts if available
        passed_count = output.count("PASSED")
        failed_count = output.count("FAILED")
        total_count = passed_count + failed_count
        
        return PytestResult(
            passed=passed,
            return_code=proc.returncode,
            output=output,
            total_tests=total_count,
            passed_tests=passed_count,
            failed_tests=failed_count
        )
    except Exception as e:
        return PytestResult(
            passed=False,
            return_code=1,
            output=f"Failed to execute pytest subprocess: {e}",
            total_tests=0,
            passed_tests=0,
            failed_tests=1
        )

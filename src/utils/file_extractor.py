import re
from pathlib import Path
from typing import List, Union

def extract_and_save_code_files(llm_output: str, target_dir: Union[str, Path]) -> List[Path]:
    """
    Extracts code blocks containing '# filename: <filename>' or labeled headers,
    writing them safely to disk in the specified target directory.
    """
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    saved_files: List[Path] = []
    
    # Primary Regex: matches ```python\n# filename: <name>\n<code>\n```
    pattern = r"```(?:python)?\s*\n#\s*filename:\s*([\w\.-]+)\n([\s\S]*?)```"
    matches = re.findall(pattern, llm_output, re.IGNORECASE)
    
    if matches:
        for filename, code in matches:
            filepath = target_path / filename.strip()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code.strip() + "\n")
            saved_files.append(filepath)
    else:
        # Secondary fallback: Extract generic python blocks and name sensibly
        blocks = re.findall(r"```(?:python)?\s*\n([\s\S]*?)```", llm_output)
        if len(blocks) >= 2:
            f1 = target_path / "insurance_engine.py"
            f2 = target_path / "prototype_app.py"
            with open(f1, "w", encoding="utf-8") as f:
                f.write(blocks[0].strip() + "\n")
            with open(f2, "w", encoding="utf-8") as f:
                f.write(blocks[1].strip() + "\n")
            saved_files.extend([f1, f2])
        elif len(blocks) == 1:
            f1 = target_path / "prototype_code.py"
            with open(f1, "w", encoding="utf-8") as f:
                f.write(blocks[0].strip() + "\n")
            saved_files.append(f1)
            
    return saved_files

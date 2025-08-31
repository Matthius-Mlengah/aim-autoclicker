from __future__ import annotations
from pathlib import Path

def load_stylesheet(qss_path: str, **vars) -> str:
    t = Path(qss_path).read_text(encoding="utf-8")
    for k, v in vars.items():
        t = t.replace("{{" + k + "}}", str(v))
    return t

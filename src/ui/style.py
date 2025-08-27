from __future__ import annotations
from importlib.resources import files

def load_stylesheet_pkg(pkg: str, name: str, **vars) -> str:
    t = (files(pkg) / name).read_text(encoding="utf-8")
    for k, v in vars.items():
        t = t.replace("{{" + k + "}}", str(v))
    return t

"""Read-only syntax/data checks; never import or execute project programs."""
import json
import subprocess
import sys
import tomllib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
paths = [root / p for p in subprocess.check_output(
    ["git", "ls-files", "-z"], cwd=root).decode().split("\0") if p]
count = 0
extra_python = {"BitwigColorPaletteGenerator"}
extra_shell = {"PKGBUILD", "derpcat-clean-storage", "derpcat-storage-status"}
for path in paths:
    if path.is_symlink() or not path.is_file():
        continue
    rel = path.relative_to(root)
    if path.suffix == ".py" or path.name in extra_python:
        compile(path.read_bytes(), str(rel), "exec")
    elif path.suffix == ".json":
        json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix == ".toml":
        tomllib.loads(path.read_text(encoding="utf-8"))
    elif path.suffix == ".sh" or path.name in extra_shell:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        shell = "sh" if first_line.startswith("#!") and first_line.endswith("/sh") else "bash"
        subprocess.run([shell, "-n", str(path)], check=True)
    else:
        continue
    count += 1
    print(f"OK {rel}")
if not count:
    sys.exit("No supported source/data files found")
print(f"Validated {count} source/data files without executing application code")

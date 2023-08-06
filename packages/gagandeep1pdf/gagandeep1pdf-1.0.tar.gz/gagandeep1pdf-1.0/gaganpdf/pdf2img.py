from pathlib import Path

p = Path("README.md").read_text()
print(p)



import sys
from pathlib import Path

current_dir = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent
repo_dir = (current_dir / "..").resolve()


assert any(repo_dir.glob(".git"))

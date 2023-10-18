import os
import subprocess

from black import main as black
from ruff.__main__ import find_ruff_bin

from app.scripts.tools.config import config


def main() -> None:
    print("\nRuff:")
    ruff = find_ruff_bin()
    subprocess.run([os.fsdecode(ruff), "--fix", *config.FORMAT_DIRS])

    print("\nBlack:")
    black.main(config.FORMAT_DIRS)


if __name__ == "__main__":
    main()

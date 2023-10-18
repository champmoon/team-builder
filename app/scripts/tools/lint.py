import os
import subprocess
import sys

from black import main as black
from mypy import main as mypy
from ruff.__main__ import find_ruff_bin

from app.scripts.tools.config import config


def main() -> None:
    print("\nRuff:")
    ruff = find_ruff_bin()
    subprocess.run([os.fsdecode(ruff), *config.LINT_DIRS])

    print("\nBlack:")
    black.main([*config.LINT_DIRS, "--check"], standalone_mode=False)

    print("\nMypy:")
    mypy.main(
        stdout=sys.stdout,
        stderr=sys.stderr,
        args=[*config.LINT_DIRS],
        clean_exit=True,
    )


if __name__ == "__main__":
    main()

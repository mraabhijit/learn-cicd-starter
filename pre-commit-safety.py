#!/usr/bin/env python

import shutil
import subprocess
import sys

uv_path = shutil.which("uv")
if not uv_path:
    raise FileNotFoundError("uv executable not found")
result = subprocess.run([uv_path, "run", "safety", "scan"], cwd=".")  # noqa: S603
sys.exit(result.returncode)

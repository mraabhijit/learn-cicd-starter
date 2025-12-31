#!/usr/bin/env python
import subprocess
import sys

result = subprocess.run(["uv", "run", "safety", "scan"], cwd=".")
sys.exit(result.returncode)

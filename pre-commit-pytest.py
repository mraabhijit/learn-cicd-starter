#!/usr/bin/env python
import subprocess
import sys

result = subprocess.run(["uv", "run", "pytest"], cwd=".")
sys.exit(result.returncode)

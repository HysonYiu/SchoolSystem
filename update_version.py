#!/usr/bin/env python3
"""
update_version.py
用法: python update_version.py 2.0.0-alpha.8 "更新描述"
自動更新 version.txt, main.py, README.md badge
"""
import sys, re

if len(sys.argv) < 2:
    print("用法: python update_version.py <version> [description]")
    sys.exit(1)

VERSION = sys.argv[1]
DESC = sys.argv[2] if len(sys.argv) > 2 else "版本更新"

# version.txt
with open("version.txt", "w") as f:
    f.write(VERSION + "\n")

# main.py
with open("main.py", "r") as f:
    src = f.read()
src = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{VERSION}"', src)
with open("main.py", "w") as f:
    f.write(src)

# README.md badge
with open("README.md", "r") as f:
    readme = f.read()
readme = re.sub(
    r'!\[Version\]\(https://img\.shields\.io/badge/version-[^)]+\)',
    f'![Version](https://img.shields.io/badge/version-{VERSION}-5856d6)',
    readme
)
with open("README.md", "w") as f:
    f.write(readme)

print(f"✅ Version bumped to {VERSION}")
print(f"   - version.txt")
print(f"   - main.py __version__")
print(f"   - README.md badge")

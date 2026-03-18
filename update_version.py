#!/usr/bin/env python3
"""
update_version.py — SchoolSystem version management
用法: python update_version.py <version> "<changelog description>"
例子: python update_version.py 2.0.0-alpha.9 "fix whiteboard Poe API"

自動更新:
  - version.txt
  - main.py __version__
  - README.md badge (正確 shields.io 格式)
  - CHANGELOG.md (加入新條目)
"""
import sys, re
from datetime import date

if len(sys.argv) < 3:
    print("用法: python update_version.py <version> \"<description>\"")
    sys.exit(1)

VERSION = sys.argv[1]
DESC    = sys.argv[2]
TODAY   = date.today().isoformat()

def shields_safe(v):
    """shields.io: hyphens → double-dash, underscores → double-underscore"""
    return v.replace("-", "--").replace("_", "__")

# ── version.txt ───────────────────────────────────────────────────────────────
with open("version.txt", "w") as f:
    f.write(VERSION + "\n")
print(f"  ✓ version.txt → {VERSION}")

# ── main.py ───────────────────────────────────────────────────────────────────
with open("main.py", "r") as f:
    src = f.read()
src = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{VERSION}"', src)
with open("main.py", "w") as f:
    f.write(src)
print(f"  ✓ main.py __version__")

# ── README.md badge ───────────────────────────────────────────────────────────
with open("README.md", "r") as f:
    readme = f.read()

badge_url = f"https://img.shields.io/badge/version-{shields_safe(VERSION)}-5856d6?style=flat-square"
readme = re.sub(
    r'!\[Version\]\(https://img\.shields\.io/badge/version-[^)]+\)',
    f'![Version]({badge_url})',
    readme
)
with open("README.md", "w") as f:
    f.write(readme)
print(f"  ✓ README.md badge")
print(f"    → {badge_url}")

# ── CHANGELOG.md ─────────────────────────────────────────────────────────────
with open("CHANGELOG.md", "r") as f:
    changelog = f.read()

# Check if version already in changelog
if f"[{VERSION}]" not in changelog:
    # Determine tag label
    if "hotfix" in VERSION:
        tag = "🔧 HOTFIX"
    elif "alpha" in VERSION:
        tag = "🧪 ALPHA"
    elif "beta" in VERSION:
        tag = "🔵 BETA"
    else:
        tag = "✅ STABLE"

    new_entry = f"""## [{VERSION}] - {TODAY} {tag}
### 更新
- {DESC}

---

"""
    # Insert after first "---" separator (after the header)
    changelog = changelog.replace("---\n\n## [", f"---\n\n{new_entry}## [", 1)
    with open("CHANGELOG.md", "w") as f:
        f.write(changelog)
    print(f"  ✓ CHANGELOG.md → [{VERSION}] {TODAY}")
else:
    print(f"  ⚠ CHANGELOG.md already has [{VERSION}], skipped")

print(f"\n✅ Version bumped to {VERSION}")

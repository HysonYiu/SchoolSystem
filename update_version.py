#!/usr/bin/env python3
"""
update_version.py
用法: python update_version.py <version> "<changelog描述>"
例子: python update_version.py 2.0.0-alpha.9 "修復白板上載，更新 watchdog"

自動更新:
  - version.txt
  - main.py __version__
  - README.md badge
  - CHANGELOG.md (加最新版本)
"""
import sys, re
from datetime import date

if len(sys.argv) < 2:
    print("用法: python update_version.py <version> [description]")
    sys.exit(1)

VERSION = sys.argv[1]
DESC    = sys.argv[2] if len(sys.argv) > 2 else "版本更新"
TODAY   = date.today().isoformat()

# Determine release type label
if "alpha" in VERSION:
    label = "🧪 Alpha"
elif "beta" in VERSION:
    label = "🔵 Beta"
elif "hotfix" in VERSION:
    label = "🔴 Hotfix"
else:
    label = "✅ Stable"

# ── version.txt ──────────────────────────────────────────────────────────────
with open("version.txt", "w") as f:
    f.write(VERSION + "\n")
print(f"  version.txt → {VERSION}")

# ── main.py ──────────────────────────────────────────────────────────────────
with open("main.py", "r") as f:
    src = f.read()
src = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{VERSION}"', src)
with open("main.py", "w") as f:
    f.write(src)
print(f"  main.py __version__ → {VERSION}")

# ── README.md badge (shields.io: hyphens → --) ───────────────────────────────
badge_ver = VERSION.replace("-", "--")
with open("README.md", "r") as f:
    readme = f.read()
readme = re.sub(
    r'!\[Version\]\(https://img\.shields\.io/badge/version-[^)]+\)',
    f'![Version](https://img.shields.io/badge/version-{badge_ver}-5856d6)',
    readme
)
with open("README.md", "w") as f:
    f.write(readme)
print(f"  README.md badge → v{VERSION}")

# ── CHANGELOG.md ──────────────────────────────────────────────────────────────
with open("CHANGELOG.md", "r") as f:
    changelog = f.read()

new_entry = f"""## [{VERSION}] - {TODAY} {label}
### 更新
- {DESC}

---

"""

# Insert after the first "---" separator (after header)
if f"## [{VERSION}]" not in changelog:
    changelog = changelog.replace(
        "---\n\n## [2.0.0-alpha.1]",
        "---\n\n" + new_entry + "## [2.0.0-alpha.1]"
    )
    if new_entry not in changelog:
        # Fallback: insert after first ---
        parts = changelog.split("---\n\n", 2)
        if len(parts) >= 2:
            changelog = parts[0] + "---\n\n" + new_entry + "---\n\n".join(parts[1:])

with open("CHANGELOG.md", "w") as f:
    f.write(changelog)
print(f"  CHANGELOG.md → added {VERSION}")

print(f"\n✅ Version bumped to {VERSION}")

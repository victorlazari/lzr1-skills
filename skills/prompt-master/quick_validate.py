#!/usr/bin/env python3
import os
import sys

def validate_skill():
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    skill_md_path = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(skill_md_path):
        print("FAIL: SKILL.md not found.")
        sys.exit(1)

    with open(skill_md_path, "r") as f:
        content = f.read()

    lines = content.split("\n")
    if len(lines) > 500:
        print(f"FAIL: SKILL.md is {len(lines)} lines, which exceeds the 500 line limit.")
        sys.exit(1)

    if "Opus 4.7" in content or "GPT-5" in content:
        print("FAIL: Fictional model versions found in SKILL.md.")
        sys.exit(1)

    print("PASS: SKILL.md validation.")
    sys.exit(0)

if __name__ == "__main__":
    validate_skill()

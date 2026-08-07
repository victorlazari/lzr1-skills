#!/usr/bin/env python3
import sys
import os
import re

def validate_prd(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    required_sections = [
        r"## Overview",
        r"## Problem Statement",
        r"## Goals and Success Metrics",
        r"## User Stories",
        r"## Requirements",
        r"## Design",
        r"## Technical Considerations",
        r"## Risks and Mitigations",
        r"## Timeline",
        r"## Open Questions"
    ]

    missing_sections = []
    for section in required_sections:
        if not re.search(section, content, re.IGNORECASE):
            missing_sections.append(section.replace("## ", ""))

    if missing_sections:
        print(f"Validation Failed: '{file_path}' is missing the following required sections:")
        for section in missing_sections:
            print(f"  - {section}")
        return False

    print(f"Validation Passed: '{file_path}' contains all required sections.")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: python3 validate-prd.py <path_to_prd.md>")
        sys.exit(1 if len(sys.argv) != 2 else 0)

    file_path = sys.argv[1]
    success = validate_prd(file_path)
    sys.exit(0 if success else 1)

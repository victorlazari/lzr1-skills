#!/usr/bin/env python3
import argparse
import json
import sys

def validate_curriculum(file_path, level):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Basic validation logic (placeholder for actual validation)
    if 'level' not in data or data['level'] != level:
        print(f"Validation failed: Curriculum level does not match {level}")
        sys.exit(1)

    if 'grammar_nodes' not in data or not data['grammar_nodes']:
        print("Validation failed: Missing grammar nodes")
        sys.exit(1)

    print(f"Validation passed for level {level}")
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a generated curriculum plan.")
    parser.add_argument("file_path", help="Path to the curriculum JSON file")
    parser.add_argument("level", help="Target CEFR or ACTFL level")
    args = parser.parse_args()

    validate_curriculum(args.file_path, args.level)

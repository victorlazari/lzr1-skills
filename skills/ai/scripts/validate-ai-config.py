#!/usr/bin/env python3
import argparse
import json
import sys
import os

try:
    import yaml
except ImportError:
    yaml = None

try:
    import toml
except ImportError:
    toml = None

def validate_json(file_path):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"PASS: {file_path} is valid JSON.")
        return True
    except Exception as e:
        print(f"FAIL: {file_path} is invalid JSON. Error: {e}")
        return False

def validate_yaml(file_path):
    if yaml is None:
        print(f"SKIP: {file_path} (PyYAML not installed)")
        return True
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        print(f"PASS: {file_path} is valid YAML.")
        return True
    except Exception as e:
        print(f"FAIL: {file_path} is invalid YAML. Error: {e}")
        return False

def validate_toml(file_path):
    if toml is None:
        print(f"SKIP: {file_path} (toml not installed)")
        return True
    try:
        with open(file_path, 'r') as f:
            toml.load(f)
        print(f"PASS: {file_path} is valid TOML.")
        return True
    except Exception as e:
        print(f"FAIL: {file_path} is invalid TOML. Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Validate AI configuration schemas (JSON, YAML, TOML).")
    parser.add_argument("files", nargs="+", help="Files to validate")
    args = parser.parse_args()

    all_passed = True
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"FAIL: File not found: {file_path}")
            all_passed = False
            continue

        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.json':
            if not validate_json(file_path):
                all_passed = False
        elif ext in ['.yaml', '.yml']:
            if not validate_yaml(file_path):
                all_passed = False
        elif ext == '.toml':
            if not validate_toml(file_path):
                all_passed = False
        else:
            print(f"WARN: Unsupported file extension for {file_path}")

    if not all_passed:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()

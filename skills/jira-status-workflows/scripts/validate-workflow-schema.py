#!/usr/bin/env python3
import json
import sys
import argparse

def validate_schema(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Basic validation for Jira workflow JSON schema
        if 'name' not in data:
            print("Error: Missing 'name' in workflow schema.")
            return False
        if 'statuses' not in data:
            print("Error: Missing 'statuses' in workflow schema.")
            return False
        if 'transitions' not in data:
            print("Error: Missing 'transitions' in workflow schema.")
            return False

        print(f"Validation successful for {file_path}")
        return True
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}")
        return False
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Jira workflow JSON schema.")
    parser.add_argument("file", help="Path to the workflow JSON file")
    args = parser.parse_args()

    if not validate_schema(args.file):
        sys.exit(1)
    sys.exit(0)

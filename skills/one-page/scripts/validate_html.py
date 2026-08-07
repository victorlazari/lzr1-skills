#!/usr/bin/env python3
import sys
import os
import argparse

def validate_html(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().lower()

    issues = []

    # Basic structural checks
    if "<html" not in content:
        issues.append("Missing <html> tag.")
    if "<head" not in content:
        issues.append("Missing <head> tag.")
    if "<body" not in content:
        issues.append("Missing <body> tag.")

    # Check for inline styles or style block (self-contained requirement)
    if "<style" not in content and "style=" not in content and "<link" not in content:
        issues.append("No styles found. Ensure the HTML is self-contained with inline styles or a <style> block.")

    if issues:
        print(f"Validation failed for '{file_path}':")
        for issue in issues:
            print(f" - {issue}")
        return False

    print(f"Validation passed for '{file_path}'.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a generated HTML one-pager.")
    parser.add_argument("file", help="Path to the HTML file to validate.")
    args = parser.parse_args()

    if not validate_html(args.file):
        sys.exit(1)
    sys.exit(0)

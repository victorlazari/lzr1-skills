#!/usr/bin/env python3
import argparse
import sys
import re

def validate_artifact(file_path, framework, dry_run=False):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return False

    if dry_run:
        print(f"[DRY RUN] Would validate '{file_path}' against '{framework}' requirements.")
        return True

    errors = []

    # General checks
    if "disclaimer" not in content.lower() and "not constitute formal legal counsel" not in content.lower():
        errors.append("Missing required legal disclaimer.")

    # Framework specific checks
    if framework.upper() == "PCI DSS":
        if "v4.0.1" not in content:
            errors.append("PCI DSS artifact must explicitly reference version v4.0.1.")
    elif framework.upper() == "CCPA":
        if "2026" not in content and "risk assessment" not in content.lower():
            errors.append("CCPA artifact must reference 2026 regulations (e.g., risk assessments, cybersecurity audits).")
    elif framework.upper() == "UK GDPR":
        if "data (use and access) act" not in content.lower():
            errors.append("UK GDPR artifact must reference the Data (Use and Access) Act 2025.")
    elif framework.upper() == "GDPR":
        if "gdpr" not in content.lower():
            errors.append("GDPR artifact must explicitly reference GDPR.")
    elif framework.upper() == "HIPAA":
        if "hipaa" not in content.lower():
            errors.append("HIPAA artifact must explicitly reference HIPAA.")
    elif framework.upper() == "SOC 2":
        if "soc 2" not in content.lower():
            errors.append("SOC 2 artifact must explicitly reference SOC 2.")
    else:
        print(f"Warning: Unknown framework '{framework}'. Performing general checks only.")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        return False

    print("Validation passed.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate compliance artifacts against framework requirements.")
    parser.add_argument("file", help="Path to the compliance artifact file to validate.")
    parser.add_argument("--framework", required=True, help="The regulatory framework (e.g., 'PCI DSS', 'CCPA', 'UK GDPR').")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actual validation.")

    args = parser.parse_args()

    success = validate_artifact(args.file, args.framework, args.dry_run)
    if not success:
        sys.exit(1)
    sys.exit(0)

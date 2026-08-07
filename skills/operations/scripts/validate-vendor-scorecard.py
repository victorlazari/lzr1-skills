#!/usr/bin/env python3
import csv
import sys
import argparse

def validate_scorecard(file_path):
    weights = {
        'Functionality Score (0-5)': 0.25,
        'Cost Score (0-5)': 0.20,
        'Security Score (0-5)': 0.15,
        'Integration Score (0-5)': 0.15,
        'Support Score (0-5)': 0.10,
        'Scalability Score (0-5)': 0.10,
        'Viability Score (0-5)': 0.05
    }

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            if not headers:
                print("Error: Empty CSV file.")
                return False

            missing_headers = [h for h in weights.keys() if h not in headers]
            if missing_headers:
                print(f"Error: Missing required columns: {', '.join(missing_headers)}")
                return False

            if 'Vendor Name' not in headers:
                print("Error: Missing 'Vendor Name' column.")
                return False

            for row_num, row in enumerate(reader, start=2):
                vendor_name = row.get('Vendor Name', f'Row {row_num}')
                total_score = 0

                for col, weight in weights.items():
                    val_str = row.get(col, '').strip()
                    if not val_str:
                        print(f"Error: Missing value for '{col}' in row {row_num} ({vendor_name}).")
                        return False
                    try:
                        val = float(val_str)
                        if not (0 <= val <= 5):
                            print(f"Error: Value {val} for '{col}' in row {row_num} ({vendor_name}) is out of range (0-5).")
                            return False
                        total_score += val * weight
                    except ValueError:
                        print(f"Error: Invalid number '{val_str}' for '{col}' in row {row_num} ({vendor_name}).")
                        return False

                print(f"Vendor '{vendor_name}' validated successfully. Weighted Score: {total_score:.2f} / 5.00")

        return True
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate a vendor scorecard CSV file.')
    parser.add_argument('file', help='Path to the vendor scorecard CSV file')
    args = parser.parse_args()

    if validate_scorecard(args.file):
        print("Validation passed.")
        sys.exit(0)
    else:
        print("Validation failed.")
        sys.exit(1)

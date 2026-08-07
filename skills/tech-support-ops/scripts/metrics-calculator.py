#!/usr/bin/env python3
"""
Metrics Calculator for Tech Support Operations

Calculates MTTA, MTTR, and Error Budget Burn Rates.
Supports dry-run mode for safe execution.
"""

import argparse
import json
import sys
from datetime import datetime

def calculate_mtta(incidents):
    """Calculate Mean Time to Acknowledge in minutes."""
    total_time = 0
    count = 0
    for incident in incidents:
        if 'created_at' in incident and 'acknowledged_at' in incident:
            try:
                created = datetime.fromisoformat(incident['created_at'].replace('Z', '+00:00'))
                acked = datetime.fromisoformat(incident['acknowledged_at'].replace('Z', '+00:00'))
                delta = (acked - created).total_seconds() / 60
                if delta >= 0:
                    total_time += delta
                    count += 1
            except ValueError:
                continue
    return total_time / count if count > 0 else 0

def calculate_mttr(incidents):
    """Calculate Mean Time to Resolve in minutes."""
    total_time = 0
    count = 0
    for incident in incidents:
        if 'created_at' in incident and 'resolved_at' in incident:
            try:
                created = datetime.fromisoformat(incident['created_at'].replace('Z', '+00:00'))
                resolved = datetime.fromisoformat(incident['resolved_at'].replace('Z', '+00:00'))
                delta = (resolved - created).total_seconds() / 60
                if delta >= 0:
                    total_time += delta
                    count += 1
            except ValueError:
                continue
    return total_time / count if count > 0 else 0

def calculate_burn_rate(slo_target, total_requests, failed_requests, time_window_hours):
    """Calculate Error Budget Burn Rate."""
    if total_requests == 0:
        return 0

    error_rate = failed_requests / total_requests
    error_budget = 1.0 - (slo_target / 100.0)

    if error_budget == 0:
        return float('inf') if error_rate > 0 else 0

    burn_rate = error_rate / error_budget
    return burn_rate

def main():
    parser = argparse.ArgumentParser(description="Calculate Tech Support Operations Metrics")
    parser.add_argument("--incidents-file", type=str, help="Path to JSON file containing incident data")
    parser.add_argument("--slo-target", type=float, help="SLO Target percentage (e.g., 99.9)")
    parser.add_argument("--total-requests", type=int, help="Total number of requests in the time window")
    parser.add_argument("--failed-requests", type=int, help="Number of failed requests in the time window")
    parser.add_argument("--time-window", type=float, default=720, help="Time window in hours (default: 720 for 30 days)")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without saving results")

    args = parser.parse_args()

    results = {}

    if args.incidents_file:
        try:
            with open(args.incidents_file, 'r') as f:
                incidents = json.load(f)
            results['MTTA_minutes'] = round(calculate_mtta(incidents), 2)
            results['MTTR_minutes'] = round(calculate_mttr(incidents), 2)
        except Exception as e:
            print(f"Error reading incidents file: {e}", file=sys.stderr)
            sys.exit(1)

    if args.slo_target is not None and args.total_requests is not None and args.failed_requests is not None:
        burn_rate = calculate_burn_rate(args.slo_target, args.total_requests, args.failed_requests, args.time_window)
        results['Error_Budget_Burn_Rate'] = round(burn_rate, 2)

    if not results:
        print("No metrics calculated. Provide either --incidents-file or SLO parameters.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    output = json.dumps(results, indent=2)

    if args.dry_run:
        print("[DRY RUN] Calculated Metrics:")
        print(output)
    else:
        print(output)

if __name__ == "__main__":
    main()

import json
import subprocess
import time
import argparse

def run_mcp_command(tool_name, input_data):
    """Execute an MCP tool via the manus-mcp-cli."""
    cmd = [
        "manus-mcp-cli", "tool", "call", tool_name,
        "--server", "calendar",
        "--input", json.dumps(input_data)
    ]

    print(f"Executing {tool_name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def process_action_plan(plan_file, dry_run=False):
    """Reads the action plan and executes updates in batches to avoid timeouts."""
    with open(plan_file, 'r') as f:
        plan = json.load(f)

    updates = plan.get('updates', [])
    deletes = plan.get('deletes', [])

    print(f"Found {len(updates)} events to update and {len(deletes)} to delete.")

    if dry_run:
        print("\n--- DRY RUN ---")
        print("Updates:")
        for u in updates:
            print(f"  - Update event {u['eventId']} to start at {u['start']['dateTime']} ({u['start']['timeZone']})")
        print("Deletes:")
        for d in deletes:
            print(f"  - Delete event {d['eventId']}")
        print("--- END DRY RUN ---")
        return

    # Process Updates in batches of 5
    batch_size = 5
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i+batch_size]
        print(f"\nProcessing update batch {i//batch_size + 1} ({len(batch)} events)...")

        for u in batch:
            input_data = {
                "eventId": u["eventId"],
                "start": u["start"],
                "end": u["end"]
            }
            success = run_mcp_command("update_event", input_data)
            if not success:
                print(f"Failed to update event {u['eventId']}! Check logs.")
            else:
                print(f"Successfully updated event {u['eventId']}.")

            # Respect API rate limits
            time.sleep(1)

    # Process Deletes
    if deletes:
        print(f"\nProcessing {len(deletes)} deletions...")
        for d in deletes:
            input_data = {
                "eventId": d["eventId"]
            }
            success = run_mcp_command("delete_event", input_data)
            if success:
                print(f"Successfully deleted event {d['eventId']}.")
            else:
                print(f"Failed to delete event {d['eventId']}! Check logs.")

            # Respect API rate limits
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch update Google Calendar events.")
    parser.add_argument("plan_file", help="Path to the action_plan.json file")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes")
    args = parser.parse_args()

    process_action_plan(args.plan_file, dry_run=args.dry_run)

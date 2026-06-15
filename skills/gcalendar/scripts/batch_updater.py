import json
import subprocess
import time

def run_mcp_command(tool_name, input_data):
    """Execute an MCP tool via the manus-mcp-cli."""
    cmd = [
        "manus-mcp-cli", "tool", "call", tool_name, 
        "--server", "google-calendar", 
        "--input", json.dumps(input_data)
    ]
    
    print(f"Executing {tool_name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def process_action_plan(plan_file):
    """Reads the action plan and executes updates in batches to avoid timeouts."""
    with open(plan_file, 'r') as f:
        plan = json.load(f)
        
    updates = plan.get('updates', [])
    deletes = plan.get('deletes', [])
    
    print(f"Found {len(updates)} events to update and {len(deletes)} to delete.")
    
    # Process Updates in batches of 5
    batch_size = 5
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i+batch_size]
        print(f"\nProcessing update batch {i//batch_size + 1} ({len(batch)} events)...")
        
        # Prepare input for google_calendar_update_events
        input_data = {
            "events": [
                {
                    "event_id": u["event_id"],
                    "start_time": u["start_time"],
                    "end_time": u["end_time"]
                } for u in batch
            ]
        }
        
        success = run_mcp_command("google_calendar_update_events", input_data)
        if not success:
            print("Batch failed! Check logs.")
        else:
            print("Batch succeeded.")
            
        # Small delay between batches
        time.sleep(2)
        
    # Process Deletes
    if deletes:
        print(f"\nProcessing {len(deletes)} deletions...")
        # Deletes are generally faster, but can still be batched if > 20
        input_data = {
            "events": [{"event_id": d["event_id"]} for d in deletes]
        }
        success = run_mcp_command("google_calendar_delete_events", input_data)
        if success:
            print("Deletions completed successfully.")
        else:
            print("Deletions failed! Check logs.")

if __name__ == "__main__":
    # Example usage
    # process_action_plan('action_plan.json')
    pass

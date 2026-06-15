import json
from datetime import datetime, timedelta
from collections import defaultdict

def normalize_team(name):
    """Normalize team names for matching, handling common aliases."""
    team_aliases = {
        "ir iran": "iran",
        "korea republic": "south korea",
        "côte d'ivoire": "ivory coast",
        "cote d'ivoire": "ivory coast",
        "cabo verde": "cape verde",
        "usa": "united states",
        "türkiye": "turkiye"
    }
    name = name.lower().strip()
    return team_aliases.get(name, name)

def normalize_match_name(summary):
    """Extract team names from calendar event summary."""
    s = summary.replace("World Cup 2026: ", "")
    if "—" in s:
        s = s.split("—")[0].strip()
    if "Opening Match" in s:
        if "(" in s and ")" in s:
            inner = s[s.index("(")+1:s.index(")")]
            if " vs " in inner:
                s = inner
        else:
            s = "Mexico vs South Africa"
    return s.strip()

def match_teams(cal_match, official_match):
    """Check if two match descriptions refer to the same game, regardless of team order."""
    cal_parts = [normalize_team(t.strip()) for t in cal_match.lower().split(" vs ")]
    off_parts = [normalize_team(t.strip()) for t in official_match.lower().split(" vs ")]
    
    if len(cal_parts) != 2 or len(off_parts) != 2:
        return False
        
    return set(cal_parts) == set(off_parts)

def validate_calendar(events_file, official_schedule_dict):
    """
    Validates calendar events against an official schedule.
    
    Args:
        events_file: Path to JSON file containing calendar events
        official_schedule_dict: Dict mapping "Team A vs Team B" to "YYYY-MM-DDTHH:MM:SS-0Z:00"
        
    Returns:
        action_plan dict with updates and deletes
    """
    with open(events_file, 'r') as f:
        events = json.load(f)
        
    event_matches = []  # List of (event_index, official_match_key, status)
    
    # 1. Map events to ground truth
    for i, event in enumerate(events):
        summary = event.get('summary', '')
        
        # Identify generic placeholders
        if "Group Stage" in summary or "match schedule" in summary:
            event_matches.append((i, None, "generic"))
            continue
            
        match_name = normalize_match_name(summary)
        found_key = None
        
        for official_match, official_time in official_schedule_dict.items():
            if match_teams(match_name, official_match):
                found_key = official_match
                break
                
        if found_key:
            start_time = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
            if start_time == official_schedule_dict[found_key]:
                event_matches.append((i, found_key, "correct"))
            else:
                event_matches.append((i, found_key, "incorrect"))
        else:
            event_matches.append((i, None, "not_found"))
            
    # 2. Handle duplicates
    match_to_events = defaultdict(list)
    for i, (idx, match_key, status) in enumerate(event_matches):
        if match_key:
            match_to_events[match_key].append(idx)
            
    duplicates_to_delete = []
    events_to_keep = {}
    
    for match_key, event_indices in match_to_events.items():
        if len(event_indices) == 1:
            events_to_keep[match_key] = event_indices[0]
        else:
            # Prefer keeping the one that already has the correct time
            correct_ones = [idx for idx in event_indices if event_matches[idx][2] == "correct"]
            if correct_ones:
                keep = correct_ones[0]
            else:
                # Fallback: keep the one with the most detailed description
                keep = max(event_indices, key=lambda idx: len(events[idx].get('description', '')))
                
            events_to_keep[match_key] = keep
            for idx in event_indices:
                if idx != keep:
                    duplicates_to_delete.append(idx)
                    
    # 3. Build Action Plan
    updates = []
    deletes = []
    
    # Add duplicates and generic events to deletes
    generic_to_delete = [idx for idx, key, status in event_matches if status == "generic"]
    all_to_delete = set(duplicates_to_delete + generic_to_delete)
    
    for idx in sorted(all_to_delete):
        deletes.append({
            "event_id": events[idx]['id'],
            "summary": events[idx]['summary']
        })
        
    # Add incorrect (but kept) events to updates
    for idx, match_key, status in event_matches:
        if status == "incorrect" and idx not in all_to_delete and idx == events_to_keep.get(match_key):
            correct_start = official_schedule_dict[match_key]
            
            # Calculate end time (e.g., 2 hours after start)
            start_dt = datetime.fromisoformat(correct_start)
            end_dt = start_dt + timedelta(hours=2)
            correct_end = end_dt.isoformat()
            
            updates.append({
                "event_id": events[idx]['id'],
                "summary": events[idx]['summary'],
                "start_time": correct_start,
                "end_time": correct_end
            })
            
    return {
        "updates": updates,
        "deletes": deletes
    }

# Example usage:
# official_schedule = {"Mexico vs South Africa": "2026-06-11T16:00:00-03:00"}
# plan = validate_calendar('events.json', official_schedule)
# with open('action_plan.json', 'w') as f:
#     json.dump(plan, f, indent=2)

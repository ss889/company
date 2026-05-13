import json
import os

# Module-level variable for file path (allows tests to override)
HISTORY_FILE = "/tmp/history.json"  # Vercel uses /tmp for writable storage


def load_history():
    """Load and return all search entries from history.json."""
    try:
        if not os.path.exists(HISTORY_FILE):
            return []
        
        with open(HISTORY_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(entries):
    """Save a list of entries to history.json."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def get_entry_by_id(entry_id):
    """Retrieve a single entry by its id."""
    history = load_history()
    for entry in history:
        if entry.get("id") == entry_id:
            return entry
    return None


def delete_entry_by_id(entry_id):
    """Delete an entry by its id and save the updated history."""
    history = load_history()
    for i, entry in enumerate(history):
        if entry.get("id") == entry_id:
            history.pop(i)
            save_history(history)
            return True
    return False

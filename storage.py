import json
import os

# Module-level variable for file path (allows tests to override)
HISTORY_FILE = "history.json"


def load_history():
    """Load and return all search entries from history.json.
    
    Returns:
        list: List of all search entries, or empty list if file missing/empty.
    """
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
    """Save a list of entries to history.json.
    
    Args:
        entries (list): List of entry dictionaries to save.
    """
    with open(HISTORY_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def get_entry_by_id(entry_id):
    """Retrieve a single entry by its id.
    
    Args:
        entry_id (str): The id of the entry to find.
        
    Returns:
        dict: The entry dict if found, None otherwise.
    """
    history = load_history()
    for entry in history:
        if entry.get("id") == entry_id:
            return entry
    return None


def delete_entry_by_id(entry_id):
    """Delete an entry by its id and save the updated history.
    
    Args:
        entry_id (str): The id of the entry to delete.
        
    Returns:
        bool: True if entry was found and deleted, False otherwise.
    """
    history = load_history()
    for i, entry in enumerate(history):
        if entry.get("id") == entry_id:
            history.pop(i)
            save_history(history)
            return True
    return False

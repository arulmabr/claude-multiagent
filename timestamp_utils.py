"""
Timestamp Utilities - Helper functions for consistent timestamp handling across agents.
"""

from datetime import datetime, timezone
import time

def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()

def get_unix_timestamp():
    """Get current Unix timestamp."""
    return int(time.time())

def parse_timestamp(timestamp_str):
    """Parse ISO format timestamp string."""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

def time_since(timestamp_str):
    """Calculate time elapsed since a given timestamp."""
    past = parse_timestamp(timestamp_str)
    now = datetime.now(timezone.utc)
    delta = now - past
    return delta.total_seconds()

def format_duration(seconds):
    """Format duration in seconds to human-readable string."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds / 60)}m {int(seconds % 60)}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"

if __name__ == "__main__":
    # Test the utilities
    now = get_timestamp()
    print(f"Current timestamp: {now}")
    print(f"Unix timestamp: {get_unix_timestamp()}")

    # Simulate some time passing
    import time
    time.sleep(2)

    elapsed = time_since(now)
    print(f"Time elapsed: {format_duration(elapsed)}")

# logs/logger.py
"""
Logger system for detection results and system events.
Currently logs to console with formatted output.
Designed for easy MongoDB integration in production.
"""

import datetime
from typing import Dict, List, Optional

# In-memory storage for recent logs (will be replaced with MongoDB)
_recent_logs = []
_max_logs_in_memory = 100  # Keep last 100 logs in memory

def log_detection(result: Dict) -> None:
    """
    Log a detection result in a formatted way to console.
    Also stores in memory for get_logs() function.
    
    Args:
        result (Dict): Detection result from pipeline.analyze_post()
                      Expected keys: post_id, trust_score, reason, timestamp
    """
    
    # Extract data from result
    post_id = result.get("post_id", "Unknown")
    trust_score = result.get("trust_score", 0)
    reason = result.get("reason", "No reason provided")
    timestamp = result.get("timestamp", datetime.datetime.utcnow().isoformat() + "Z")
    
    # Format trust score with color coding for console
    trust_display = _format_trust_score(trust_score)
    
    # Create formatted log message
    log_message = f"[AI-Agent] Post #{post_id} → Trust Score: {trust_display} → Reason: {reason}"
    
    # Print to console
    print(log_message)
    
    # Store in memory for get_logs() (will be replaced with MongoDB insert)
    _store_log_in_memory(result, log_message)

def _format_trust_score(trust_score: int) -> str:
    """
    Format trust score with percentage and optional color indicators.
    
    Args:
        trust_score (int): Trust score from 0-100
        
    Returns:
        str: Formatted trust score string
    """
    
    # Convert to percentage
    percentage = f"{trust_score}%"
    
    # Add visual indicators based on trust level
    if trust_score >= 80:
        return f"{percentage} ✅"  # High trust - green checkmark
    elif trust_score >= 60:
        return f"{percentage} ⚠️"   # Medium-high trust - warning
    elif trust_score >= 40:
        return f"{percentage} ❓"   # Medium trust - question mark
    elif trust_score >= 20:
        return f"{percentage} ⚠️"   # Low trust - warning
    else:
        return f"{percentage} 🚨"   # Very low trust - alert
    
def _store_log_in_memory(result: Dict, formatted_message: str) -> None:
    """
    Store log entry in memory for retrieval.
    This will be replaced with MongoDB insertion in production.
    
    Args:
        result (Dict): Original detection result
        formatted_message (str): Formatted console message
    """
    
    global _recent_logs
    
    # Create log entry for storage
    log_entry = {
        "id": len(_recent_logs) + 1,  # Simple incrementing ID
        "post_id": result.get("post_id"),
        "trust_score": result.get("trust_score"),
        "reason": result.get("reason"),
        "timestamp": result.get("timestamp"),
        "formatted_message": formatted_message,
        "logged_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    
    # Add to recent logs
    _recent_logs.append(log_entry)
    
    # Keep only recent logs (prevent memory overflow)
    if len(_recent_logs) > _max_logs_in_memory:
        _recent_logs.pop(0)  # Remove oldest log

def get_logs(limit: Optional[int] = 20) -> List[Dict]:
    """
    Retrieve recent detection logs.
    Currently returns from in-memory storage.
    In production, this will query MongoDB with pagination.
    
    Args:
        limit (int, optional): Maximum number of logs to return. Defaults to 20.
        
    Returns:
        List[Dict]: List of recent log entries
    """
    
    # Return recent logs (most recent first)
    recent_logs = _recent_logs[-limit:] if _recent_logs else []
    recent_logs.reverse()  # Most recent first
    
    return recent_logs

def get_logs_by_trust_range(min_trust: int = 0, max_trust: int = 100, limit: int = 20) -> List[Dict]:
    """
    Get logs filtered by trust score range.
    Placeholder for MongoDB query with filtering.
    
    Args:
        min_trust (int): Minimum trust score (inclusive)
        max_trust (int): Maximum trust score (inclusive) 
        limit (int): Maximum number of results
        
    Returns:
        List[Dict]: Filtered log entries
    """
    
    # Filter logs by trust score range
    filtered_logs = [
        log for log in _recent_logs 
        if min_trust <= log.get("trust_score", 0) <= max_trust
    ]
    
    # Return most recent first, limited
    filtered_logs.reverse()
    return filtered_logs[:limit]

def get_logs_summary() -> Dict:
    """
    Get summary statistics of recent logs.
    In production, this will use MongoDB aggregation.
    
    Returns:
        Dict: Summary statistics
    """
    
    if not _recent_logs:
        return {
            "total_logs": 0,
            "avg_trust_score": 0,
            "high_trust_count": 0,
            "medium_trust_count": 0, 
            "low_trust_count": 0,
            "latest_log_time": None
        }
    
    # Calculate statistics
    trust_scores = [log.get("trust_score", 0) for log in _recent_logs]
    total_logs = len(_recent_logs)
    avg_trust = sum(trust_scores) / total_logs if trust_scores else 0
    
    # Count by trust levels
    high_trust = sum(1 for score in trust_scores if score >= 70)
    medium_trust = sum(1 for score in trust_scores if 30 <= score < 70)
    low_trust = sum(1 for score in trust_scores if score < 30)
    
    # Get latest timestamp
    latest_log = _recent_logs[-1] if _recent_logs else None
    latest_time = latest_log.get("timestamp") if latest_log else None
    
    return {
        "total_logs": total_logs,
        "avg_trust_score": round(avg_trust, 1),
        "high_trust_count": high_trust,
        "medium_trust_count": medium_trust,
        "low_trust_count": low_trust,
        "latest_log_time": latest_time
    }

def log_system_event(event_type: str, message: str, details: Optional[Dict] = None) -> None:
    """
    Log system events (agent start/stop, errors, etc.).
    
    Args:
        event_type (str): Type of event (e.g., "AGENT_START", "ERROR", "INFO")
        message (str): Event message
        details (Dict, optional): Additional event details
    """
    
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    # Format system event message
    formatted_message = f"[{event_type}] {message}"
    if details:
        formatted_message += f" | Details: {details}"
    
    # Print to console
    print(f"[{timestamp}] {formatted_message}")
    
    # In production, this would also go to MongoDB system events collection

def clear_logs() -> int:
    """
    Clear all logs from memory.
    In production, this would be a MongoDB delete operation with safety checks.
    
    Returns:
        int: Number of logs cleared
    """
    
    global _recent_logs
    cleared_count = len(_recent_logs)
    _recent_logs.clear()
    
    log_system_event("MAINTENANCE", f"Cleared {cleared_count} logs from memory")
    return cleared_count

# MongoDB integration placeholder functions
def _init_mongodb_connection():
    """
    Initialize MongoDB connection.
    This will replace the in-memory storage system.
    """
    # TODO: Implement MongoDB connection
    # from pymongo import MongoClient
    # client = MongoClient(mongodb_uri)
    # db = client.misinformation_detection
    # return db.detection_logs
    pass

def _insert_log_to_mongodb(log_entry: Dict):
    """
    Insert log entry to MongoDB collection.
    
    Args:
        log_entry (Dict): Log entry to insert
    """
    # TODO: Implement MongoDB insertion
    # collection.insert_one(log_entry)
    pass

def _query_logs_from_mongodb(filter_dict: Dict, limit: int, sort_by: str = "timestamp"):
    """
    Query logs from MongoDB with filtering and sorting.
    
    Args:
        filter_dict (Dict): MongoDB query filter
        limit (int): Result limit
        sort_by (str): Field to sort by
        
    Returns:
        List[Dict]: Query results
    """
    # TODO: Implement MongoDB query
    # return list(collection.find(filter_dict).sort(sort_by, -1).limit(limit))
    pass

# Test function to demonstrate the logger
def test_logger():
    """Test function to demonstrate logging functionality."""
    print("🧪 Testing detection logger...\n")
    
    # Sample detection results to log
    test_results = [
        {
            "post_id": 1,
            "trust_score": 85,
            "reason": "High confidence authentic text content",
            "timestamp": "2025-07-30T14:30:00.000000Z"
        },
        {
            "post_id": 2,
            "trust_score": 23,
            "reason": "Multiple red flags found in video. Deepfake detection confidence: 89%",
            "timestamp": "2025-07-30T14:31:00.000000Z"
        },
        {
            "post_id": 3,
            "trust_score": 67,
            "reason": "Moderate confidence in audio authenticity. Voice pattern analysis pending",
            "timestamp": "2025-07-30T14:32:00.000000Z"
        },
        {
            "post_id": 4,
            "trust_score": 12,
            "reason": "Strong misinformation indicators detected. Cross-modal mismatch",
            "timestamp": "2025-07-30T14:33:00.000000Z"
        }
    ]
    
    # Log each result
    print("📊 Logging detection results:")
    for result in test_results:
        log_detection(result)
    
    print("\n" + "="*80)
    
    # Test log retrieval
    print("\n📜 Recent logs (get_logs()):")
    recent_logs = get_logs(limit=3)
    for log in recent_logs:
        print(f"  Log #{log['id']}: {log['formatted_message']}")
    
    print("\n" + "="*80)
    
    # Test filtering by trust score
    print("\n🚨 Low trust logs (0-30%):")
    low_trust_logs = get_logs_by_trust_range(min_trust=0, max_trust=30)
    for log in low_trust_logs:
        print(f"  {log['formatted_message']}")
    
    print("\n" + "="*80)
    
    # Test summary statistics
    print("\n📈 Logs Summary:")
    summary = get_logs_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*80)
    
    # Test system events
    print("\n🔧 System Events:")
    log_system_event("AGENT_START", "Autonomous agent initialized successfully")
    log_system_event("ERROR", "Database connection timeout", {"retry_count": 3, "timeout": "5s"})
    log_system_event("INFO", "Processing batch completed", {"posts_processed": 150})

if __name__ == "__main__":
    test_logger()
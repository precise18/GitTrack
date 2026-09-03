"""
Test script for DynamoDB operations.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Get the project root directory - works with both direct run and exec()
try:
    # Try to get the script directory
    script_dir = Path(__file__).parent.parent
except NameError:
    # If __file__ is not defined (when using exec), use current directory
    script_dir = Path.cwd()

# Add paths
sys.path.insert(0, str(script_dir))
sys.path.insert(0, str(script_dir / 'src'))

# Import db with fallback
try:
    from src.db import db
    print("✅ Imported db from src.db")
except ImportError:
    try:
        from db import db
        print("✅ Imported db from db")
    except ImportError as e:
        print(f"❌ Could not import db: {e}")
        print(f"   Current Python path: {sys.path[:3]}")
        print(f"   Script directory: {script_dir}")
        print(f"   src/db.py exists: {(script_dir / 'src' / 'db.py').exists()}")
        sys.exit(1)

def insert_test_data():
    """Insert test data into DynamoDB"""
    print("\n📊 Inserting test data into DynamoDB...")
    
    # Test students with different activity levels
    students = [
        ("Alice Chen", 5, 2, "2026-08-25T10:00:00Z"),
        ("Alice Chen", 8, 3, "2026-08-24T14:00:00Z"),
        ("Alice Chen", 3, 1, "2026-08-23T09:30:00Z"),
        ("Bob Smith", 3, 1, "2026-08-25T11:30:00Z"),
        ("Bob Smith", 7, 2, "2026-08-24T15:00:00Z"),
        ("Charlie Brown", 2, 0, "2026-08-25T09:15:00Z"),
        ("Charlie Brown", 4, 1, "2026-08-24T13:45:00Z"),
        ("Diana Prince", 6, 2, "2026-08-25T14:20:00Z"),
        ("Eve Wilson", 1, 0, "2026-08-25T16:30:00Z"),
    ]
    
    for student_id, commits, mr, timestamp in students:
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            db.save_activity(
                student_id=student_id,
                timestamp=dt,
                commits=commits,
                merge_requests=mr,
                project_id="123"
            )
        except Exception as e:
            print(f"❌ Error saving {student_id}: {e}")
    
    print("✅ Test data insertion complete!")

def query_data():
    """Query and display data"""
    print("\n🔍 Querying data...")
    
    try:
        # Get all students
        students = db.get_all_students()
        print(f"\n📋 Students in database: {', '.join(students) if students else 'None found'}")
        
        # Get all activity
        all_activity = db.get_all_activity()
        print(f"\n📊 Total records: {len(all_activity)}")
        
        # Show activity for each student
        for student in students:
            items = db.get_student_activity(student)
            total_commits = sum(item.get('commits', 0) for item in items)
            total_mrs = sum(item.get('merge_requests', 0) for item in items)
            print(f"\n👤 {student}:")
            print(f"   - Total commits: {total_commits}")
            print(f"   - Total merge requests: {total_mrs}")
            print(f"   - Days active: {len(items)}")
    except Exception as e:
        print(f"❌ Error querying: {e}")

if __name__ == "__main__":
    print("🔍 GitTrack DynamoDB Test")
    print("=" * 40)
    insert_test_data()
    query_data()
    print("\n✅ Test complete!")

"""
Generate mock commit data for testing GitTrack.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_mock_commits(num_commits=50, days_back=7):
    """Generate mock commit data"""
    
    students = [
        {'name': 'Alice Chen', 'email': 'alice@example.com'},
        {'name': 'Bob Smith', 'email': 'bob@example.com'},
        {'name': 'Charlie Brown', 'email': 'charlie@example.com'},
        {'name': 'Diana Prince', 'email': 'diana@example.com'},
        {'name': 'Eve Wilson', 'email': 'eve@example.com'},
    ]
    
    mock_data = []
    now = datetime.now()
    
    commit_messages = [
        "Fix bug in authentication",
        "Update README documentation",
        "Add new feature for dashboard",
        "Refactor code for better performance",
        "Fix failing tests",
        "Update dependencies",
        "Add error handling",
        "Improve UI design",
        "Optimize database queries",
        "Add logging functionality"
    ]
    
    for i in range(num_commits):
        student = random.choice(students)
        
        # Random date in the last 7 days
        days_ago = random.randint(0, days_back)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        commit_date = now - timedelta(
            days=days_ago, 
            hours=hours_ago, 
            minutes=minutes_ago
        )
        
        commit = {
            'id': f'mock_commit_{i}_{random.randint(1000, 9999)}',
            'short_id': f'{random.randint(100000, 999999)}',
            'author_name': student['name'],
            'author_email': student['email'],
            'created_at': commit_date.isoformat() + 'Z',
            'message': f"#{i} {random.choice(commit_messages)}",
            'title': f"Commit #{i}",
            'project_id': 123456,
            'web_url': f"https://mock.gitlab.com/project/commit/{i}"
        }
        mock_data.append(commit)
    
    # Sort by date (newest first)
    return sorted(mock_data, key=lambda x: x['created_at'], reverse=True)

def save_mock_data():
    """Generate and save mock data"""
    commits = generate_mock_commits(50)
    
    # Save to file
    data_path = Path(__file__).parent.parent / 'data' / 'mock_commits.json'
    with open(data_path, 'w') as f:
        json.dump(commits, f, indent=2)
    
    print(f"✅ Generated {len(commits)} mock commits")
    print(f"📁 Saved to {data_path}")
    
    # Show statistics
    from collections import Counter
    counts = Counter(c['author_name'] for c in commits)
    print("\n📊 Commit Distribution:")
    for student, count in counts.most_common():
        print(f"  - {student}: {count} commits ({count/len(commits)*100:.1f}%)")
    
    return commits

if __name__ == "__main__":
    save_mock_data()

"""
Fetch commits from GitLab or use mock data.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to path so we can import src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import config from src package
try:
    from src import config
    CONFIG = config  # config is the instance, not the class
except ImportError as e:
    print(f"❌ Could not import config module: {e}")
    sys.exit(1)

def fetch_commits():
    """Fetch commits from configured source"""
    
    if CONFIG.USE_MOCK_DATA:
        print("📊 Using mock data...")
        return fetch_mock_commits()
    else:
        print("🔗 Fetching from GitLab...")
        return fetch_gitlab_commits()

def fetch_mock_commits():
    """Load mock commits from file"""
    data_path = project_root / 'data' / 'mock_commits.json'
    
    try:
        with open(data_path, 'r') as f:
            commits = json.load(f)
        print(f"✅ Loaded {len(commits)} mock commits")
        return commits
    except FileNotFoundError:
        print("❌ Mock data file not found. Running generator...")
        os.system('python scripts/generate_mock_data.py')
        return fetch_mock_commits()

def fetch_gitlab_commits():
    """Fetch real commits from GitLab API"""
    import requests
    
    headers = {'PRIVATE-TOKEN': CONFIG.GITLAB_TOKEN}
    
    # Get commits from the last 7 days
    since_date = (datetime.now() - timedelta(days=7)).isoformat()
    
    url = f"{CONFIG.GITLAB_URL}/api/v4/projects/{CONFIG.GITLAB_PROJECT_ID}/repository/commits"
    params = {
        'since': since_date,
        'per_page': 100
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        commits = response.json()
        print(f"✅ Fetched {len(commits)} commits from GitLab")
        return commits
    except Exception as e:
        print(f"❌ Error fetching commits: {e}")
        return []

def analyze_commits(commits):
    """Analyze commit data and return metrics"""
    from collections import Counter, defaultdict
    
    # Count commits per student
    student_counts = Counter(c.get('author_name', 'Unknown') for c in commits)
    
    # Commits per day
    daily_counts = defaultdict(int)
    for commit in commits:
        try:
            date = datetime.fromisoformat(commit['created_at'].replace('Z', '+00:00'))
            day = date.strftime('%Y-%m-%d')
            daily_counts[day] += 1
        except:
            pass
    
    return {
        'total_commits': len(commits),
        'students': list(student_counts.keys()),
        'student_commit_counts': dict(student_counts),
        'daily_commit_counts': dict(daily_counts),
        'most_active_student': max(student_counts.items(), key=lambda x: x[1])[0] if student_counts else None
    }

if __name__ == "__main__":
    print("🔍 GitTrack Commit Fetcher\n" + "="*40)
    
    # Fetch commits
    commits = fetch_commits()
    
    if commits:
        # Analyze
        metrics = analyze_commits(commits)
        
        print("\n📊 Analysis Results:")
        print(f"  - Total Commits: {metrics['total_commits']}")
        print(f"  - Students: {', '.join(metrics['students'])}")
        print(f"  - Most Active: {metrics['most_active_student']}")
        print(f"  - Daily Distribution: {len(metrics['daily_commit_counts'])} days with commits")
        
        print("\n📈 Student Commit Distribution:")
        for student, count in metrics['student_commit_counts'].items():
            percentage = (count / metrics['total_commits']) * 100
            bar = '█' * int(percentage / 5)
            print(f"  {student:20} {bar} {count} commits ({percentage:.1f}%)")
    else:
        print("❌ No commits found!")

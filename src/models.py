"""
Data models for GitTrack.
"""

from datetime import datetime
from typing import Dict, List, Optional

class StudentActivity:
    def __init__(self, student_id: str, timestamp: datetime, 
                 commits: int = 0, merge_requests: int = 0):
        self.student_id = student_id
        self.timestamp = timestamp
        self.commits = commits
        self.merge_requests = merge_requests
    
    def to_dict(self) -> Dict:
        return {
            'student_id': self.student_id,
            'timestamp': self.timestamp.isoformat(),
            'commits': self.commits,
            'merge_requests': self.merge_requests
        }
    
    @classmethod
    def from_commit(cls, commit: Dict) -> 'StudentActivity':
        """Create activity from GitLab commit data"""
        return cls(
            student_id=commit.get('author_name', 'Unknown'),
            timestamp=datetime.fromisoformat(commit['created_at'].replace('Z', '+00:00')),
            commits=1,
            merge_requests=0
        )

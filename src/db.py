"""
DynamoDB operations for GitTrack.
"""

import boto3
from datetime import datetime
from typing import List, Dict, Optional
import json

class DynamoDBClient:
    def __init__(self, table_name: str = "StudentActivity", region: str = "us-east-1"):
        self.table_name = table_name
        self.region = region
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(table_name)
        self.client = boto3.client('dynamodb', region_name=region)
    
    def save_activity(self, student_id: str, timestamp: datetime, 
                      commits: int = 0, merge_requests: int = 0,
                      project_id: str = "123") -> None:
        """Save student activity to DynamoDB"""
        item = {
            'student_id': student_id,
            'timestamp': timestamp.isoformat() + 'Z',
            'commits': commits,
            'merge_requests': merge_requests,
            'project_id': project_id
        }
        try:
            self.table.put_item(Item=item)
            print(f"✅ Saved activity for {student_id}")
        except Exception as e:
            print(f"❌ Error saving: {e}")
    
    def get_student_activity(self, student_id: str) -> List[Dict]:
        """Get all activity for a student"""
        try:
            response = self.table.query(
                KeyConditionExpression='student_id = :id',
                ExpressionAttributeValues={':id': student_id}
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"❌ Error querying: {e}")
            return []
    
    def get_activity_by_date_range(self, student_id: str, 
                                   start_date: datetime, 
                                   end_date: datetime) -> List[Dict]:
        """Get activity for a student within a date range"""
        try:
            response = self.table.query(
                KeyConditionExpression='student_id = :id AND timestamp BETWEEN :start AND :end',
                ExpressionAttributeValues={
                    ':id': student_id,
                    ':start': start_date.isoformat() + 'Z',
                    ':end': end_date.isoformat() + 'Z'
                }
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"❌ Error querying: {e}")
            return []
    
    def get_all_students(self) -> List[str]:
        """Get unique student IDs"""
        try:
            response = self.table.scan(ProjectionExpression='student_id')
            return list(set(item['student_id'] for item in response.get('Items', [])))
        except Exception as e:
            print(f"❌ Error scanning: {e}")
            return []
    
    def get_all_activity(self) -> List[Dict]:
        """Get all activity records"""
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except Exception as e:
            print(f"❌ Error scanning: {e}")
            return []

# Create a global client instance
db = DynamoDBClient()

if __name__ == "__main__":
    print("🔍 Testing DynamoDB connection...")
    try:
        # Test connection
        tables = db.client.list_tables()
        print(f"✅ Connected to DynamoDB in {db.region}")
        print(f"   Tables: {tables.get('TableNames', [])}")
        
        # Get all students
        students = db.get_all_students()
        print(f"   Students found: {students}")
        
        # Get all activity
        all_activity = db.get_all_activity()
        print(f"   Total records: {len(all_activity)}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

import requests
import json
from datetime import datetime

class NotionTracker:
    def __init__(self, token, database_id):
        self.token = token
        self.database_id = database_id
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
    
    def update_page_status(self, page_id, status):
        """Update page status in Notion database"""
        url = f'https://api.notion.com/v1/pages/{page_id}'
        
        data = {
            'properties': {
                'Status': {
                    'select': {'name': status}
                },
                'Last Updated': {
                    'date': {'start': datetime.now().isoformat()}
                }
            }
        }
        
        response = requests.patch(url, headers=self.headers, json=data)
        
        if response.status_code == 200:
            print(f'Successfully updated page {page_id} to status: {status}')
            return True
        else:
            print(f'Failed to update page: {response.content}')
            return False
    
    def create_shot_entry(self, shot_name, artist, deadline, priority='Medium'):
        """Create new shot entry in Notion database"""
        url = f'https://api.notion.com/v1/pages'
        
        data = {
            'parent': {'database_id': self.database_id},
            'properties': {
                'Shot Name': {
                    'title': [{'text': {'content': shot_name}}]
                },
                'Artist': {
                    'rich_text': [{'text': {'content': artist}}]
                },
                'Deadline': {
                    'date': {'start': deadline}
                },
                'Priority': {
                    'select': {'name': priority}
                },
                'Status': {
                    'select': {'name': 'Not Started'}
                }
            }
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 200:
            print(f'Created new shot entry: {shot_name}')
            return response.json()
        else:
            print(f'Failed to create shot entry: {response.content}')
            return None

if __name__ == '__main__':
    # Example usage
    notion_token = 'your_notion_token_here'
    database_id = 'your_database_id_here'
    
    tracker = NotionTracker(notion_token, database_id)
    
    # Create new shot entry
    tracker.create_shot_entry('Shot_002', 'Jane Smith', '2025-09-01', 'High')
    
    # Update existing page
    page_id = 'your_page_id_here'
    tracker.update_page_status(page_id, 'In Progress')

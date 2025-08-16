import json
from datetime import datetime, timedelta

class AssetDeliveryTracker:
    def __init__(self, json_file='asset_tracker.json'):
        self.json_file = json_file
        self.load_data()
    
    def load_data(self):
        """Load tracking data from JSON file"""
        try:
            with open(self.json_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {'assets': [], 'deliveries': []}
    
    def save_data(self):
        """Save tracking data to JSON file"""
        with open(self.json_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_asset(self, asset_name, asset_type, artist, deadline):
        """Add new asset to tracking system"""
        asset = {
            'id': len(self.data['assets']) + 1,
            'name': asset_name,
            'type': asset_type,
            'artist': artist,
            'deadline': deadline,
            'status': 'Not Started',
            'created': datetime.now().isoformat(),
            'versions': []
        }
        
        self.data['assets'].append(asset)
        self.save_data()
        print(f'Added asset: {asset_name}')
    
    def update_asset_status(self, asset_id, status, notes=''):
        """Update asset status"""
        for asset in self.data['assets']:
            if asset['id'] == asset_id:
                asset['status'] = status
                asset['last_updated'] = datetime.now().isoformat()
                if notes:
                    asset['notes'] = notes
                self.save_data()
                print(f'Updated asset {asset["name"]} to status: {status}')
                return True
        
        print(f'Asset with ID {asset_id} not found')
        return False
    
    def get_upcoming_deadlines(self, days=7):
        """Get assets with deadlines in the next X days"""
        upcoming = []
        cutoff_date = datetime.now() + timedelta(days=days)
        
        for asset in self.data['assets']:
            deadline = datetime.fromisoformat(asset['deadline'])
            if deadline <= cutoff_date and asset['status'] != 'Completed':
                days_left = (deadline - datetime.now()).days
                asset['days_left'] = days_left
                upcoming.append(asset)
        
        return sorted(upcoming, key=lambda x: x['days_left'])
    
    def generate_progress_report(self):
        """Generate progress report for all assets"""
        total_assets = len(self.data['assets'])
        completed = len([a for a in self.data['assets'] if a['status'] == 'Completed'])
        in_progress = len([a for a in self.data['assets'] if a['status'] == 'In Progress'])
        not_started = len([a for a in self.data['assets'] if a['status'] == 'Not Started'])
        
        report = {
            'total_assets': total_assets,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'completion_rate': f'{(completed/total_assets)*100:.1f}%' if total_assets > 0 else '0%'
        }
        
        return report

if __name__ == '__main__':
    tracker = AssetDeliveryTracker()
    
    # Add some sample assets
    tracker.add_asset('Character_Model_Hero', 'Model', 'Artist A', '2025-09-15')
    tracker.add_asset('Environment_City', 'Environment', 'Artist B', '2025-09-20')
    
    # Update status
    tracker.update_asset_status(1, 'In Progress', 'Started modeling')
    
    # Check upcoming deadlines
    upcoming = tracker.get_upcoming_deadlines(30)
    print(f'Upcoming deadlines: {len(upcoming)} assets')
    
    # Generate report
    report = tracker.generate_progress_report()
    print('Progress Report:', report)

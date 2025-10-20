# test_integration.py
import sys
import os
sys.path.append('.')

from app import app
import json

def test_integration():
    print("🧪 Testing DataProcessor Integration...")
    
    with app.test_client() as client:
        # Test 1: Add a user
        print("\n1. Testing user creation:")
        response = client.post('/add_user', json={'name': 'TestUser'})
        print(f"Add user response: {response.get_json()}")
        
        # Test 2: Add a post with hashtags
        print("\n2. Testing post creation with DataProcessor:")
        response = client.post('/add_post', json={
            'user': 'TestUser', 
            'content': 'Loving this #awesome #project! So #happy'
        })
        print(f"Add post response: {response.get_json()}")
        
        # Test 3: Get data and check processed info
        print("\n3. Testing data retrieval with processed info:")
        response = client.get('/get_data')
        data = response.get_json()
        print(f"Processed stats: {data.get('processed_stats', {})}")
        print(f"Trending hashtags: {data.get('trending_hashtags', [])}")
        
        # Test 4: Test advanced analytics
        print("\n4. Testing advanced analytics:")
        response = client.get('/analytics/trending')
        analytics = response.get_json()
        print(f"Analytics response: {analytics}")
        
        print("\n✅ Integration test completed!")

if __name__ == '__main__':
    test_integration()
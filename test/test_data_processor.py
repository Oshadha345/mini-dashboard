# test_comprehensive.py
import sys
import os
sys.path.append('.')

from app import app
import json

def test_comprehensive():
    print("🧪 Comprehensive DataProcessor Integration Test...")
    
    with app.test_client() as client:
        # Clear any existing data by restarting would be better, but for now we'll work with what we have
        
        # Test 1: Add multiple posts with different sentiments and hashtags
        print("\n1. Adding multiple test posts...")
        test_posts = [
            {'user': 'Alice', 'content': 'Having a #great day! #sunshine #happy'},
            {'user': 'Bob', 'content': 'Not feeling well today #sad #weather'},
            {'user': 'Charlie', 'content': 'Working on my #project #coding #excited'},
            {'user': 'Diana', 'content': 'This is just a normal post without hashtags'},
            {'user': 'Alice', 'content': 'Another #happy post with #sunshine'}
        ]
        
        for post_data in test_posts:
            response = client.post('/add_post', json=post_data)
            print(f"Added post by {post_data['user']}: {response.status_code}")
        
        # Test 2: Check basic data
        print("\n2. Checking basic data...")
        response = client.get('/get_data')
        data = response.get_json()
        print(f"Total users: {len(data['users'])}")
        print(f"Total posts: {len(data['posts'])}")
        print(f"Processed stats: {data['processed_stats']}")
        print(f"Trending hashtags: {data['trending_hashtags']}")
        
        # Test 3: Test advanced analytics
        print("\n3. Testing advanced analytics endpoint...")
        response = client.get('/analytics/trending')
        analytics = response.get_json()
        
        if 'error' in analytics:
            print(f"❌ Analytics error: {analytics['error']}")
        else:
            print(f"✅ Analytics successful!")
            print(f"   Total posts analyzed: {analytics['total_posts_analyzed']}")
            print(f"   Sentiment distribution: {analytics['sentiment_distribution']}")
            print(f"   Top trending: {[t['hashtag'] for t in analytics['trending_hashtags'][:3]]}")
        
        # Test 4: Test likes and engagement
        print("\n4. Testing engagement...")
        if data['posts']:
            first_post_id = data['posts'][0]['id']
            response = client.post('/like_post', json={'post_id': first_post_id})
            print(f"Like post response: {response.get_json()}")
        
        print("\n🎉 Comprehensive test completed!")

if __name__ == '__main__':
    test_comprehensive()
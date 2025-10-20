from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import json
import time
import sys
import os

# Add algorithms to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))
from data_processor import DataProcessor

app = Flask(__name__)

# Simple storage (in real app, use database)
users = {}
posts = []
friendships = defaultdict(set)
processed_posts = []  # Store processed posts for analysis

# Add some sample users
sample_users = ['Alice', 'Bob', 'Charlie', 'Diana']
for user in sample_users:
    users[user] = {'name': user, 'posts': []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json.get('name')
    if name and name not in users:
        users[name] = {'name': name, 'posts': []}
        return jsonify({'success': True, 'users': list(users.keys())})
    return jsonify({'success': False, 'error': 'User exists or invalid name'})

@app.route('/add_post', methods=['POST'])
def add_post():
    user = request.json.get('user')
    content = request.json.get('content')
    
    if user in users and content:
        # Create raw post
        raw_post = {
            'user': user,
            'content': content,
            'likes': 0,
            'id': len(posts),
            'timestamp': time.time()
        }
        posts.append(raw_post)
        users[user]['posts'].append(raw_post)
        
        # PROCESS WITH DataProcessor
        processed_result = DataProcessor.process_real_time_posts([{
            'text': content,
            'timestamp': time.time(),
            'user': user
        }])
        
        if processed_result:
            processed_post = processed_result[0]  # Get first (and only) processed post
            
            # Add additional metadata
            processed_post['user'] = user
            processed_post['likes'] = 0
            processed_post['id'] = raw_post['id']
            processed_post['original'] = raw_post  # Store reference to original
            processed_posts.append(processed_post)
        
        return jsonify({
            'success': True, 
            'post': raw_post
        })
    return jsonify({'success': False})

@app.route('/add_friend', methods=['POST'])
def add_friend():
    user1 = request.json.get('user1')
    user2 = request.json.get('user2')
    
    if user1 in users and user2 in users and user1 != user2:
        friendships[user1].add(user2)
        friendships[user2].add(user1)
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/like_post', methods=['POST'])
def like_post():
    post_id = request.json.get('post_id')
    
    if 0 <= post_id < len(posts):
        posts[post_id]['likes'] += 1
        # Also update processed posts if exists
        for proc_post in processed_posts:
            if proc_post['id'] == post_id:
                proc_post['likes'] = posts[post_id]['likes']
                break
        return jsonify({'success': True, 'likes': posts[post_id]['likes']})
    return jsonify({'success': False})

@app.route('/get_data', methods=['GET'])
def get_data():
    # Calculate simple influence score (friends + total likes)
    influence_scores = {}
    for user in users:
        friend_count = len(friendships[user])
        total_likes = sum(post['likes'] for post in users[user]['posts'])
        influence_scores[user] = friend_count * 2 + total_likes
    
    # Use DataProcessor for trending analysis (if we have posts)
    trending_hashtags = []
    if posts:
        # Convert to format DataProcessor expects
        posts_for_analysis = [{'text': post['content']} for post in posts[-20:]]  # Last 20 posts
        trending_hashtags = DataProcessor.detect_trending_hashtags(posts_for_analysis, window_size=10, top_n=5)
    
    return jsonify({
        'users': list(users.keys()),
        'posts': posts[-10:],  # Last 10 posts
        'friendships': {user: list(friends) for user, friends in friendships.items()},
        'influence': dict(sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)),
        'trending_hashtags': trending_hashtags,
        'processed_stats': {
            'total_processed': len(processed_posts),
            'recent_sentiment': get_recent_sentiment(),
            'avg_word_count': get_avg_word_count()
        },
        'processed_posts': processed_posts[-10:]  # Send last 10 processed posts
    })

# Helper functions for DataProcessor analytics
def get_recent_sentiment():
    if not processed_posts:
        return 'neutral'
    
    recent = processed_posts[-5:]  # Last 5 posts
    sentiments = [p['sentiment'] for p in recent]
    
    positive = sentiments.count('positive')
    negative = sentiments.count('negative')
    
    if positive > negative:
        return 'positive'
    elif negative > positive:
        return 'negative'
    else:
        return 'neutral'

def get_avg_word_count():
    if not processed_posts:
        return 0
    recent = processed_posts[-5:]
    return sum(p['word_count'] for p in recent) / len(recent)

# NEW ENDPOINT: Advanced DataProcessor Analytics
@app.route('/analytics/trending', methods=['GET'])
def get_trending_analytics():
    """Advanced trending analysis using DataProcessor"""
    if not processed_posts:
        return jsonify({'error': 'No posts to analyze'})
    
    try:
        # FIXED: Use clean_text instead of original['text']
        posts_for_analysis = [{'text': post['clean_text']} for post in processed_posts]
        
        trending = DataProcessor.detect_trending_hashtags(
            posts_for_analysis, 
            window_size=min(20, len(processed_posts)), 
            top_n=10
        )
        
        # Engagement analysis
        engagement_data = []
        for post in processed_posts[-20:]:  # Last 20 posts
            engagement_data.append({
                'likes': post.get('likes', 0),
                'shares': 0,  # We don't track shares yet
                'comments': 0  # We don't track comments yet
            })
        
        window_analysis = []
        if engagement_data and len(engagement_data) >= 3:  # Need at least 3 for window analysis
            window_analysis = DataProcessor.sliding_window_analysis(
                engagement_data, 
                window_size=min(5, len(engagement_data)), 
                step_size=1
            )
        
        return jsonify({
            'trending_hashtags': trending,
            'engagement_analysis': window_analysis,
            'total_posts_analyzed': len(processed_posts),
            'sentiment_distribution': get_sentiment_distribution()
        })
    
    except Exception as e:
        return jsonify({'error': f'Analytics error: {str(e)}'})

def get_sentiment_distribution():
    if not processed_posts:
        return {}
    
    sentiments = [p['sentiment'] for p in processed_posts]
    return {
        'positive': sentiments.count('positive'),
        'negative': sentiments.count('negative'), 
        'neutral': sentiments.count('neutral'),
        'total': len(sentiments)
    }

if __name__ == '__main__':
    print("🚀 Starting Simple Social Network with DataProcessor...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
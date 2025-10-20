class DataProcessor:
    """
    Real-time data processing engine for hackathon
    Specialized in streaming data, pattern matching, and efficient algorithms
    """
    
    @staticmethod
    def sliding_window_max(arr, k):
        """
        Calculate maximum in all sliding windows of size k
        Input: [1, 3, -1, -3, 5, 3, 6, 7], k=3
        Output: [3, 3, 5, 5, 6, 7]
        """
        from collections import deque
        if not arr or k == 0:
            return []
        if k == 1:
            return arr
        
        result = []
        dq = deque()
        
        # First window
        for i in range(k):
            while dq and arr[i] >= arr[dq[-1]]:
                dq.pop()
            dq.append(i)
        result.append(arr[dq[0]])
        
        # Remaining windows
        for i in range(k, len(arr)):
            # Remove elements outside current window
            if dq and dq[0] <= i - k:
                dq.popleft()
            
            # Remove smaller elements
            while dq and arr[i] >= arr[dq[-1]]:
                dq.pop()
            
            dq.append(i)
            result.append(arr[dq[0]])
        
        return result
    
    @staticmethod
    def process_real_time_data(data_stream, window_size=5):
        """
        Process continuous data stream using sliding window
        Returns: statistics for each window
        """
        window = []
        results = []
        
        for data_point in data_stream:
            window.append(data_point)
            if len(window) > window_size:
                window.pop(0)
            
            if len(window) == window_size:
                stats = {
                    'max': max(window),
                    'min': min(window),
                    'avg': sum(window) / len(window),
                    'trend': 'increasing' if window[-1] > window[0] else 'decreasing'
                }
                results.append(stats)
        
        return results
    
    @staticmethod
    def kmp_search(text, pattern):
        """
        Knuth-Morris-Pratt string search algorithm
        Returns all positions where pattern is found
        """
        def build_lps(pattern):
            lps = [0] * len(pattern)
            length = 0
            i = 1
            
            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1
            return lps
        
        if not pattern or not text:
            return []
        
        lps = build_lps(pattern)
        result = []
        i = j = 0
        
        while i < len(text):
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == len(pattern):
                result.append(i - j)
                j = lps[j - 1]
            elif i < len(text) and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return result
    
    @staticmethod
    def two_sum_sorted(arr, target):
        """
        Two-pointer technique for sorted array
        Input: [2, 7, 11, 15], target=9
        Output: (0, 1)
        """
        left, right = 0, len(arr) - 1
        
        while left < right:
            current_sum = arr[left] + arr[right]
            if current_sum == target:
                return (left, right)
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return (-1, -1)
    
    @staticmethod
    def detect_anomalies(data_stream, threshold=2.0):
        """
        Real-time anomaly detection using sliding window statistics
        """
        if len(data_stream) < 3:
            return []
        
        anomalies = []
        window = data_stream[-5:]  # Last 5 points
        
        if len(window) >= 3:
            mean = sum(window) / len(window)
            std_dev = (sum((x - mean) ** 2 for x in window) / len(window)) ** 0.5
            
            current_value = data_stream[-1]
            if std_dev > 0 and abs(current_value - mean) > threshold * std_dev:
                anomalies.append({
                    'index': len(data_stream) - 1,
                    'value': current_value,
                    'mean': mean,
                    'std_dev': std_dev
                })
        
        return anomalies
        
    @staticmethod
    def process_real_time_posts(post_stream):
        """
        Clean and filter social media posts
        
        Args:
            post_stream: List of post dictionaries with 'text', 'timestamp', etc.
            
        Returns:
            List of processed post dictionaries with additional metadata
        """
        processed_posts = []
        
        for post in post_stream:
            # Skip posts that don't have required fields
            if 'text' not in post:
                continue
                
            # Clean text (remove excessive spaces, normalize)
            text = post['text']
            text = ' '.join(text.split())  # Remove extra whitespace
            
            # Extract hashtags
            hashtags = []
            words = text.split()
            for word in words:
                if word.startswith('#'):
                    # Remove punctuation at the end if any
                    clean_tag = word.rstrip('.,!?:;')
                    if len(clean_tag) > 1:  # Avoid single # with no text
                        hashtags.append(clean_tag.lower())
            
            # Extract mentions
            mentions = []
            for word in words:
                if word.startswith('@'):
                    clean_mention = word.rstrip('.,!?:;')
                    if len(clean_mention) > 1:
                        mentions.append(clean_mention.lower())
            
            # Calculate sentiment (simplified version)
            # In a real implementation, use a proper NLP library
            positive_words = {'good', 'great', 'excellent', 'amazing', 'love', 'happy', 'best'}
            negative_words = {'bad', 'poor', 'terrible', 'worst', 'hate', 'sad', 'awful'}
            
            word_set = set(w.lower() for w in words)
            positive_count = len(word_set.intersection(positive_words))
            negative_count = len(word_set.intersection(negative_words))
            
            sentiment = 'neutral'
            if positive_count > negative_count:
                sentiment = 'positive'
            elif negative_count > positive_count:
                sentiment = 'negative'
            
            # Create processed post
            processed_post = {
                'original': post,
                'clean_text': text,
                'hashtags': hashtags,
                'mentions': mentions,
                'sentiment': sentiment,
                'word_count': len(words),
                'timestamp': post.get('timestamp', None)
            }
            
            processed_posts.append(processed_post)
            
        return processed_posts
    
    @staticmethod
    def detect_trending_hashtags(text_stream, window_size=50, top_n=10):
        """
        Find popular hashtags in a stream of social media posts
        
        Args:
            text_stream: List of post dictionaries with 'text' field
            window_size: Number of recent posts to consider
            top_n: Number of top hashtags to return
            
        Returns:
            List of dictionaries with trending hashtags and their counts
        """
        # Use only the most recent posts within the window size
        recent_posts = text_stream[-window_size:] if len(text_stream) > window_size else text_stream
        
        # Extract all hashtags from the posts
        all_hashtags = []
        for post in recent_posts:
            if 'text' not in post:
                continue
                
            words = post['text'].split()
            hashtags = [word.lower() for word in words if word.startswith('#')]
            all_hashtags.extend(hashtags)
        
        # Count the occurrences of each hashtag
        hashtag_counts = {}
        for tag in all_hashtags:
            # Clean the hashtag (remove punctuation at the end)
            clean_tag = tag.rstrip('.,!?:;')
            if len(clean_tag) > 1:  # Avoid single # with no text
                hashtag_counts[clean_tag] = hashtag_counts.get(clean_tag, 0) + 1
        
        # Sort hashtags by count (descending)
        sorted_hashtags = sorted(
            hashtag_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Return the top N trending hashtags
        trending = [{'hashtag': tag, 'count': count} for tag, count in sorted_hashtags[:top_n]]
        return trending
    
    @staticmethod
    def sliding_window_analysis(interaction_data, window_size=10, step_size=1):
        """
        Track engagement patterns using sliding window analysis
        
        Args:
            interaction_data: List of dictionaries with engagement metrics
            window_size: Size of the sliding window
            step_size: Steps to move the window forward
            
        Returns:
            List of dictionaries with window statistics
        """
        if not interaction_data or len(interaction_data) < window_size:
            return []
            
        results = []
        
        # Slide the window across the data
        for i in range(0, len(interaction_data) - window_size + 1, step_size):
            window = interaction_data[i:i+window_size]
            
            # Collect engagement metrics from the window
            likes = [item.get('likes', 0) for item in window]
            shares = [item.get('shares', 0) for item in window]
            comments = [item.get('comments', 0) for item in window]
            
            # Calculate statistics
            window_stats = {
                'window_start': i,
                'window_end': i + window_size - 1,
                'avg_likes': sum(likes) / len(likes) if likes else 0,
                'avg_shares': sum(shares) / len(shares) if shares else 0,
                'avg_comments': sum(comments) / len(comments) if comments else 0,
                'total_engagement': sum(likes) + sum(shares) + sum(comments),
                'engagement_trend': 'increasing' if sum(likes[-3:] + shares[-3:] + comments[-3:]) > 
                                   sum(likes[:3] + shares[:3] + comments[:3]) else 'decreasing'
            }
            
            # Detect spikes in engagement
            avg_engagement = (window_stats['avg_likes'] + window_stats['avg_shares'] + 
                             window_stats['avg_comments']) / 3
            
            last_point = window[-1]
            last_engagement = last_point.get('likes', 0) + last_point.get('shares', 0) + last_point.get('comments', 0)
            
            if last_engagement > 2 * avg_engagement:
                window_stats['spike_detected'] = True
            else:
                window_stats['spike_detected'] = False
                
            results.append(window_stats)
            
        return results
import urllib.parse
import requests
import re

def get_youtube_search_url(query):
    """
    Generate YouTube search URL for a query
    
    Args:
        query (str): Search query (song name + artist)
        
    Returns:
        str: YouTube search URL
    """
    encoded_query = urllib.parse.quote(query)
    return f"https://www.youtube.com/results?search_query={encoded_query}"

def get_youtube_video_id(query):
    """
    Get YouTube video ID from search query using YouTube search
    
    Args:
        query (str): Search query (song name + artist)
        
    Returns:
        str: YouTube video ID or None
    """
    try:
        # Use YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        
        # Make request
        response = requests.get(search_url, timeout=5)
        
        # Extract video ID from response
        # Look for videoId in the page source
        video_id_match = re.search(r'"videoId":"([^"]{11})"', response.text)
        
        if video_id_match:
            return video_id_match.group(1)
        
        return None
    except Exception as e:
        print(f"Error fetching YouTube video ID: {e}")
        return None

def format_number(num):
    """
    Format large numbers into readable format (K, M, B)
    
    Args:
        num (int): Number to format
        
    Returns:
        str: Formatted number string
    """
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

def truncate_text(text, max_length=50):
    """
    Truncate text to specified length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_popularity_color(popularity):
    """
    Get color based on popularity score
    
    Args:
        popularity (int): Popularity score (0-100)
        
    Returns:
        str: Color code
    """
    if popularity >= 80:
        return "#1DB954"  # Green
    elif popularity >= 60:
        return "#FFA500"  # Orange
    elif popularity >= 40:
        return "#FFD700"  # Gold
    else:
        return "#808080"  # Gray
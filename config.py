"""
Configuration file for Music Discovery Hub
"""

import os

# Spotify API Configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', 'Enter Your Client ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', 'Enter Your Client Secret')

# App Configuration
APP_TITLE = "Music Discovery Hub"
APP_ICON = "🎵"
PAGE_LAYOUT = "wide"

# Search Configuration
DEFAULT_SEARCH_LIMIT_SONGS = 20
DEFAULT_SEARCH_LIMIT_ARTISTS = 10
TOP_TRACKS_LIMIT = 10
RECOMMENDATIONS_LIMIT = 10

# UI Configuration
FEATURED_ARTISTS_COUNT = 12
GRID_COLUMNS_SONGS = 4
GRID_COLUMNS_ARTISTS = 4
GRID_COLUMNS_RECOMMENDATIONS = 5

# Colors
PRIMARY_COLOR = "#1DB954"  # Spotify Green
SECONDARY_COLOR = "#667eea"
ACCENT_COLOR = "#764ba2"

# Image Configuration
DEFAULT_IMAGE_URL = "https://i.postimg.cc/0QNxYz4V/social.png"
IMAGE_SIZE_CIRCULAR = "150px"

# Model Configuration
MODEL_DF_PATH = "df.pkl"
MODEL_SIMILARITY_PATH = "similarity.pkl"

# API Configuration
SPOTIFY_MARKET = "US"
REQUEST_TIMEOUT = 30  # seconds

# Cache Configuration
CACHE_TTL = 3600  # 1 hour in seconds

# Error Messages
ERROR_MODEL_NOT_FOUND = "❌ Model files not found! Please ensure df.pkl and similarity.pkl are in the directory."
ERROR_SPOTIFY_INIT = "Failed to initialize Spotify API"
ERROR_NO_RESULTS = "No results found. Try a different search term."
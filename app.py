import streamlit as st
import pickle
import pandas as pd
from spotify_api import SpotifyAPI
from utils import get_youtube_search_url, format_number, get_youtube_video_id
import time

# Page configuration
st.set_page_config(
    page_title="Vibe Zone",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Refined aesthetic CSS with beige/grey/cream palette
st.markdown("""
            
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pattaya&family=Poppins:wght@300;400;600;700&display=swap');
       

    body, .stApp, .main, .stTextInput input, .stSelectbox > div, .stButton button, .stMarkdown {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
   
    .hero-subtitle, .section-title, .stat-label, .song-card-title, .song-card-artist {
        font-family: 'Poppins', sans-serif !important;
    }


    
    .main {
        background-color: #F5F5F0;
        color: #2C2C2C;
    }
    
    .stApp {
        background-color: #F5F5F0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #2C2C2C !important;
        font-weight: 700;
    }
    
    
    /* Hero Section with Minimal Animation */
    .hero-section {
        background: linear-gradient(135deg, #E8DFD0 0%, #D9CFC0 100%);
        padding: 100px 32px;
        border-radius: 16px;
        margin-bottom: 48px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(128,128,128,0.15) 0%, transparent 90%);
        animation: subtleRotate 20s linear infinite;
    }
    
    @keyframes subtleRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    

    .hero-title {
        font-family: "Pattaya", cursive !important ;
        font-size: 90px !important;
        font-weight: 400 !important;
        color: #2C2C2C;
        margin: 0;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 20px;
        color: #5A5A5A;
        margin-top: 16px;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Filter Section */
    .filter-section {
        background-color: #FEFEF9;
        padding: 32px;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Navigation Buttons */
    .nav-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        background-color: #D9CFC0;
        color: #2C2C2C;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 20px;
        text-decoration: none;
    }
    
    .nav-button:hover {
        background-color: #C5BCB0;
        transform: scale(1.05);
    }
    
    .nav-button:disabled {
        opacity: 0.3;
        cursor: not-allowed;
    }
    
    /* Song Card with Hover Effect */
    .song-card {
        background-color: #FEFEF9;
        border-radius: 12px;
        padding: 0;
        transition: all 0.3s ease;
        cursor: pointer;
        margin-bottom: 24px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        aspect-ratio: 1;
        position: relative;
        text-decoration: none;
        display: block;
    }
    
    .song-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .song-card-image {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    
    .song-card-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: all 0.3s ease;
    }
    
    .song-card:hover .song-card-image img {
        transform: scale(1.05);
    }
    
    .song-card-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 60%);
        opacity: 0;
        transition: opacity 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 20px;
    }
    
    .song-card:hover .song-card-overlay {
        opacity: 1;
    }
    
    .song-card-title {
        color: #FFFFFF;
        font-size: 16px;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .song-card-artist {
        color: #E0E0E0;
        font-size: 14px;
        font-weight: 400;
        margin-top: 4px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Stat Cards */
    .stat-card {
        background-color: #FEFEF9;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        height: 100%;
    }
    
    .stat-number {
        font-size: 28px;
        font-weight: 700;
        color: #8B7D6B;
    }
    
    .stat-label {
        font-size: 12px;
        color: #7A7A7A;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* Section Title */
    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #2C2C2C;
        margin: 40px 0 24px 0;
    }
    
    /* Back Button */
    .back-button {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #D9CFC0;
        color: #2C2C2C;
        padding: 12px 20px;
        border-radius: 24px;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .back-button:hover {
        background-color: #C5BCB0;
        transform: translateX(-4px);
    }
    
    /* Spotify Logo Button */
    .spotify-play-container {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background-color: #1DB954;
        padding: 12px 24px;
        border-radius: 24px;
        text-decoration: none;
        transition: all 0.3s ease;
        margin-top: 16px;
    }
    
    .spotify-play-container:hover {
        background-color: #1ed760;
        transform: scale(1.05);
    }
    
    .spotify-logo {
        width: 24px;
        height: 24px;
    }
    
    .spotify-text {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* YouTube Container */
    .youtube-container {
        background-color: #FEFEF9;
        padding: 32px;
        border-radius: 12px;
        margin: 32px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background-color: #FEFEF9;
        color: #2C2C2C;
        border-radius: 8px;
        border: 1px solid #D9CFC0;
    }
    
    /* Page info */
    .page-info {
        color: #5A5A5A;
        font-size: 14px;
        text-align: center;
        padding: 16px 0;
    }
    
    /* Artist Header */
    .artist-header {
        background: linear-gradient(135deg, #D9CFC0 0%, #E8DFD0 100%);
        padding: 60px 32px;
        border-radius: 16px;
        margin-bottom: 32px;
    }
    
    /* Match percentage */
    .match-percentage {
        color: #8B7D6B;
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    /* Custom Search Bar Styling */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #FEFEF9 0%, #F8F8F3 100%);
        border: 2px solid #E8DFD0;
        border-radius: 50px;
        padding: 16px 24px 16px 50px;
        font-size: 16px;
        color: #2C2C2C;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #C5BCB0;
        box-shadow: 0 4px 16px rgba(139, 125, 107, 0.15);
        outline: none;
        background: #FFFFFF;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9A9A9A;
        font-weight: 400;
    }
    
    /* Search Container */
    .search-container {
        position: relative;
        margin-bottom: 24px;
    }
    
    .search-icon {
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 20px;
        color: #8B7D6B;
        pointer-events: none;
        z-index: 10;
    }
    
    /* Search Label Enhancement */
    .stTextInput > label {
        display: none;
    }
    
    /* Filter Section Enhancement */
    .filter-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }
    
    .filter-icon {
        font-size: 24px;
        color: #8B7D6B;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page_home' not in st.session_state:
    st.session_state.current_page_home = 0

# Load pickle files
@st.cache_resource
def load_model_data():
    try:
        df = pickle.load(open('df.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return df, similarity
    except FileNotFoundError:
        st.error("❌ Model files not found! Please ensure df.pkl and similarity.pkl are in the directory.")
        return None, None

# Initialize Spotify API
@st.cache_resource
def init_spotify():
    return SpotifyAPI()

spotify_api = init_spotify()
df, similarity = load_model_data()

def get_recommendations(song_name, top_n=10):
    """Get song recommendations based on similarity"""
    if df is None or similarity is None:
        return []
    
    try:
        song_name_clean = song_name.strip().lower()
        matches = df[df['song'].str.lower().str.strip() == song_name_clean]
        
        if len(matches) == 0:
            matches = df[df['song'].str.lower().str.contains(song_name_clean, na=False, regex=False)]
        
        if len(matches) == 0:
            import re
            song_name_clean = re.sub(r'[^a-z0-9\s]', '', song_name_clean)
            df_clean = df['song'].str.lower().apply(lambda x: re.sub(r'[^a-z0-9\s]', '', x))
            matches = df[df_clean.str.contains(song_name_clean, na=False, regex=False)]
        
        if len(matches) == 0:
            return []
        
        idx = matches.index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
        
        recommendations = []
        for i in distances[1:top_n+1]:
            song_data = df.iloc[i[0]]
            recommendations.append({
                'song': song_data['song'],
                'artist': song_data['artist'],
                'similarity': i[1]
            })
        
        return recommendations
    except Exception as e:
        return []

def show_home_page():
    """Home page with hero section and dataset exploration"""
    
    # Hero Section
    st.markdown("""
        <div class='hero-section'>
            <h1 class='hero-title' style="font-family: 'Pattaya', 'Poppins', sans-serif; font-size: 90px;">Vibe Zone</h1>
            <p class='hero-subtitle' >Where you listen to what you feel !!!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Filter Section
    if df is not None:
        st.markdown("""
            
        """, unsafe_allow_html=True)
        
        # Custom Search Container with Icon
        st.markdown("""
            <div class='search-container'>
                <style>
                    .stTextInput > div > div {
                        position: relative;
                    }
                    .stTextInput > div > div::before {
                        content: '🔍';
                        position: absolute;
                        left: 20px;
                        top: 50%;
                        transform: translateY(-50%);
                        font-size: 20px;
                        z-index: 10;
                        pointer-events: none;
                    }
                </style>
            </div>
        """, unsafe_allow_html=True)
        
        # Search bar
        search_query = st.text_input("search", placeholder="Search songs or artists...", key='search_input', label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        
        with col1:
            all_artists = ['All Artists'] + sorted(df['artist'].unique().tolist())
            filter_artist = st.selectbox("Artist", all_artists, key='artist_filter')
        
        with col2:
            sort_by = st.selectbox("Sort By", ['Name', 'Artist', 'Random'], key='sort_filter')
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply search filter
        if search_query:
            search_lower = search_query.lower()
            filtered_df = filtered_df[
                filtered_df['song'].str.lower().str.contains(search_lower, na=False) |
                filtered_df['artist'].str.lower().str.contains(search_lower, na=False)
            ]
            # Reset pagination when search is applied
            st.session_state.current_page_home = 0
        
        if filter_artist != 'All Artists':
            filtered_df = filtered_df[filtered_df['artist'] == filter_artist]
        
        # Apply sorting
        if sort_by == 'Name':
            filtered_df = filtered_df.sort_values('song')
        elif sort_by == 'Artist':
            filtered_df = filtered_df.sort_values('artist')
        elif sort_by == 'Random':
            filtered_df = filtered_df.sample(frac=1)
        
        # Display filtered songs
        st.markdown(f"<div class='section-title'>All Songs ({len(filtered_df)} tracks)</div>", unsafe_allow_html=True)
        
        # Show message if no results
        if len(filtered_df) == 0:
            st.info("No songs found matching your search criteria. Try a different search term.")
            return
        
        # Pagination
        items_per_page = 20
        total_pages = (len(filtered_df) - 1) // items_per_page + 1
        
        # Ensure current page is within bounds
        if st.session_state.current_page_home >= total_pages:
            st.session_state.current_page_home = total_pages - 1
        
        # Page navigation with arrows
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            page_cols = st.columns([1, 1, 2, 1, 1])
            with page_cols[0]:
                if st.button("◀◀", key="first", disabled=(st.session_state.current_page_home == 0)):
                    st.session_state.current_page_home = 0
                    st.rerun()
            with page_cols[1]:
                if st.button("◀", key="prev", disabled=(st.session_state.current_page_home == 0)):
                    st.session_state.current_page_home -= 1
                    st.rerun()
            with page_cols[2]:
                st.markdown(f"<p class='page-info'>Page {st.session_state.current_page_home + 1} of {total_pages}</p>", unsafe_allow_html=True)
            with page_cols[3]:
                if st.button("▶", key="next", disabled=(st.session_state.current_page_home >= total_pages - 1)):
                    st.session_state.current_page_home += 1
                    st.rerun()
            with page_cols[4]:
                if st.button("▶▶", key="last", disabled=(st.session_state.current_page_home >= total_pages - 1)):
                    st.session_state.current_page_home = total_pages - 1
                    st.rerun()
        
        # Get current page items
        start_idx = st.session_state.current_page_home * items_per_page
        end_idx = min(start_idx + items_per_page, len(filtered_df))
        page_df = filtered_df.iloc[start_idx:end_idx]
        
        # Display songs in grid
        cols = st.columns(5)
        for idx, (df_idx, row) in enumerate(page_df.iterrows()):
            with cols[idx % 5]:
                search_results = spotify_api.search_tracks(f"{row['song']} {row['artist']}", limit=1)
                
                # Get image URL
                if search_results and search_results[0]['image_url']:
                    img_url = search_results[0]['image_url']
                else:
                    img_url = "https://via.placeholder.com/300x300/D9CFC0/2C2C2C?text=♪"
                
                # Create clickable card with query parameter
                song_id = f"{df_idx}"
                card_html = f"""
                    <a href="?selected={song_id}" target="_self" class='song-card'>
                        <div class='song-card-image'>
                            <img src='{img_url}' alt='{row["song"]}'>
                            <div class='song-card-overlay'>
                                <div class='song-card-title'>{row['song'][:30]}</div>
                                <div class='song-card-artist'>{row['artist'][:30]}</div>
                            </div>
                        </div>
                    </a>
                """
                st.markdown(card_html, unsafe_allow_html=True)

def show_song_detail_page(song_idx):
    """Detailed song page with recommendations"""
    # Get song data from dataframe
    row = df.iloc[song_idx]
    
    # Search for song details on Spotify
    search_results = spotify_api.search_tracks(f"{row['song']} {row['artist']}", limit=1)
    
    if search_results:
        song = search_results[0]
    else:
        song = {
            'name': row['song'],
            'artist': row['artist'],
            'image_url': None,
            'popularity': 'N/A',
            'album': 'Unknown',
            'release_date': 'N/A',
            'external_url': None
        }
    
    # Back button with link
    st.markdown("""
        <a href="?" target="_self" style="display: inline-flex; align-items: center; gap: 8px; background-color: #D9CFC0; color: #2C2C2C; padding: 12px 20px; border-radius: 24px; text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.3s ease;">
            ← Back
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Song header
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if song.get('image_url'):
            st.markdown(f"<img src='{song['image_url']}' style='width: 100%; max-width: 350px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);'>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color: #D9CFC0; width: 100%; max-width: 350px; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; border-radius: 12px;'><p style='font-size: 72px;'>🎵</p></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<p style='color: #7A7A7A; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>Song</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 42px; margin: 0 0 16px 0;'>{song['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px; color: #5A5A5A; font-weight: 600;'>{song['artist']}</p>", unsafe_allow_html=True)
        
        # Stats with equal grid
        stat_cols = st.columns(3)
        with stat_cols[0]:
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{song.get('popularity', 'N/A')}</div><div class='stat-label'>Popularity</div></div>", unsafe_allow_html=True)
        with stat_cols[1]:
            st.markdown(f"<div class='stat-card'><div class='stat-number' style='font-size: 16px;'>{song.get('album', 'N/A')[:20]}</div><div class='stat-label'>Album</div></div>", unsafe_allow_html=True)
        with stat_cols[2]:
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{str(song.get('release_date', 'N/A'))[:4]}</div><div class='stat-label'>Year</div></div>", unsafe_allow_html=True)
        
        # Spotify play button with logo
        if song.get('external_url'):
            st.markdown(f"""
                <a href='{song['external_url']}' target='_blank' class='spotify-play-container'>
                    <svg class='spotify-logo' viewBox="0 0 24 24" fill="#FFFFFF">
                        <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                    </svg>
                    <span class='spotify-text'>Play on Spotify</span>
                </a>
            """, unsafe_allow_html=True)
    
    # YouTube section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Watch on YouTube</div>", unsafe_allow_html=True)
    
    video_id = get_youtube_video_id(f"{song['name']} {song['artist']}")
    
    if video_id:
        st.markdown("<div class='youtube-container'>", unsafe_allow_html=True)
        st.markdown(f"""
            <iframe width="100%" height="450" 
            src="https://www.youtube.com/embed/{video_id}" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen
            style="border-radius: 12px;">
            </iframe>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Recommended Songs</div>", unsafe_allow_html=True)
    
    with st.spinner("Finding similar songs..."):
        recommendations = get_recommendations(song['name'], top_n=10)
        
        if recommendations:
            cols = st.columns(5)
            for idx, rec in enumerate(recommendations):
                with cols[idx % 5]:
                    search_results = spotify_api.search_tracks(f"{rec['song']} {rec['artist']}", limit=1)
                    
                    if search_results and search_results[0]['image_url']:
                        img_url = search_results[0]['image_url']
                    else:
                        img_url = "https://via.placeholder.com/300x300/D9CFC0/2C2C2C?text=♪"
                    
                    # Find the song index in dataframe
                    rec_match = df[(df['song'] == rec['song']) & (df['artist'] == rec['artist'])]
                    if len(rec_match) > 0:
                        rec_idx = rec_match.index[0]
                        
                        # Display clickable card with match percentage
                        rec_card_html = f"""
                            <a href="?selected={rec_idx}" target="_self" class='song-card'>
                                <div class='song-card-image'>
                                    <img src='{img_url}' alt='{rec["song"]}'>
                                    <div class='song-card-overlay'>
                                        <div class='song-card-title'>{rec['song'][:25]}</div>
                                        <div class='song-card-artist'>{rec['artist'][:25]}</div>
                                        <div class='match-percentage'>Match: {rec['similarity']:.0%}</div>
                                    </div>
                                </div>
                            </a>
                        """
                        st.markdown(rec_card_html, unsafe_allow_html=True)
        else:
            st.info("No recommendations available for this song.")

# Main app logic
def main():
    if df is None or similarity is None:
        st.error("Failed to load model data. Please check your pickle files.")
        return
    
    # Check for query parameters
    query_params = st.query_params
    
    if 'selected' in query_params:
        try:
            song_idx = int(query_params['selected'])
            if 0 <= song_idx < len(df):
                show_song_detail_page(song_idx)
            else:
                st.error("Invalid song selection")
                show_home_page()
        except (ValueError, IndexError):
            st.error("Invalid song selection")
            show_home_page()
    else:
        show_home_page()

if __name__ == "__main__":
    main()
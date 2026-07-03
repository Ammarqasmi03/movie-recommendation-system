import streamlit as st
import requests
import pickle

# ==========================================
# 1. PAGE CONFIGURATION & THEME SETUP
# ==========================================
st.set_page_config(
    page_title="Cinematic AI | Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Netflix-Inspired Custom CSS Injection
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            
    
     /* Import Font Awesome Icons */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Core Base Theme Overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #070B1B !important;
        font-family: 'Inter', sans-serif;
        color: #FFFFFF !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(7, 11, 27, 0.8);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b112c !important;
        border-right: 1px solid rgba(124, 58, 237, 0.2);
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    
    /* Hero Banner Collage */
    .hero-banner {
        background: linear-gradient(180deg, rgba(7, 11, 27, 0.1) 0%, #070B1B 95%), 
                    url('https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1925&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        height: 280px;
        border-radius: 18px;
        margin-bottom: -50px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Typography & Headers */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 5px;
        background: linear-gradient(45deg, #FFFFFF, #B3B3B3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        text-align: center;
        color: #B3B3B3;
        margin-bottom: 40px;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-vertical: 30px;
        color: #FFFFFF;
        border-left: 5px solid #E50914;
        padding-left: 15px;
    }
    
    /* Input Elements UI Customization */
    div[data-baseweb="select"] {
        background-color: #111827 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
    }
    
    div[data-baseweb="select"]:hover {
        border-color: #7C3AED !important;
    }
    
    /* Primary CTA Button Design */
    .stButton > button {
        background: linear-gradient(90deg, #E50914 0%, #B80710 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
        display: block;
        margin: 0 auto !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6) !important;
    }
    
    /* Movie Card Component Container */
    .movie-card {
        background-color: #111827;
        border-radius: 18px;
        padding: 0px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        margin-bottom: 20px;
    }
    
    .movie-card:hover {
        transform: translateY(-10px);
        border-color: #7C3AED;
        box-shadow: 0 15px 30px rgba(124, 58, 237, 0.3);
    }
    
    /* Poster Image Fit Wrapper */
    .poster-container {
        position: relative;
        width: 100%;
        padding-top: 150%; /* 2:3 Aspect Ratio */
        overflow: hidden;
    }
    
    .poster-container img {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        object-fit: cover;
    }
    
    /* Card Metadata */
    .movie-info {
        padding: 15px;
    }
    
    .movie-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .movie-meta-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.8rem;
        color: #B3B3B3;
    }
    
    .rating-badge {
        background-color: rgba(255, 191, 0, 0.15);
        color: #FFBF00;
        padding: 2px 6px;
        border-radius: 6px;
        font-weight: 600;
    }
    
    .genre-tag {
        font-size: 0.75rem;
        color: #7C3AED;
        font-weight: 500;
        margin-top: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

         


    /* Premium Cinematic Footer */
    .netflix-footer {
        margin-top: 100px;
        padding: 40px 20px;
        background-color: #0b112c;
        border-top: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 18px 18px 0 0;
        text-align: center;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 30px;
        flex-wrap: wrap;
        margin-bottom: 20px;
        align-items: center;
    }
    
    .footer-link {
        color: #B3B3B3 !important;
        text-decoration: none !important;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px; /* Space between logo and text */
    }
    
    .footer-link i {
        font-size: 1.1rem;
    }
    
    .footer-link:hover {
        color: #7C3AED !important;
        transform: translateY(-2px);
    }
    
    .footer-brand {
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 8px;
        background: linear-gradient(45deg, #E50914, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer-copyright {
        color: #6B7280;
        font-size: 0.8rem;
    }
            
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DATA UTILITIES & API INTEGRATIONS
# ==========================================
TMDB_API_KEY = "5ae6b5a09d756780f6c1fe7dcfa82bb0" # Replace with your actual key/token

def fetch_movie_meta(movie_id):
    """
    Fetches rich analytical metadata & artwork paths from the TMDB API.
    Gracefully returns fallbacks if the endpoint fails or keys are missing.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    fallback_poster = "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=500&auto=format&fit=crop"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else fallback_poster
            
            # Extract meta strings securely
            release_date = data.get('release_date', 'N/A')
            year = release_date.split('-')[0] if '-' in release_date else 'N/A'
            rating = round(data.get('vote_average', 0.0), 1)
            genres = [g['name'] for g in data.get('genres', [])[:1]]
            genre_str = genres[0] if genres else "Drama"
            
            return full_path, year, rating, genre_str
    except Exception:
       pass
    return fallback_poster, "N/A", "N/A", "General"        
    


# ==========================================
# 3. BACKEND INTEGRATION HOOKS
# ==========================================
@st.cache_data
def load_backend_data():
    """
    Safely binds localized data pickles.
    Replace filenames with your exact storage paths.
    """
    # Replace these lines with your actual pickle loaders:
    movies_df = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    # Mocking structural format matching user prompt specification for safe boots:
    import pandas as pd
    mock_data = {
        'movie_id': [19995, 285, 206647, 49026, 49529],
        'title': ['Avatar', "Pirates of the Caribbean: At World's End", 'Spectre', 'The Dark Knight Rises', 'John Carter'],
        'tags': ['text summary samples'] * 5
    }
    return movies_df, similarity

try:
    movies, similarity = load_backend_data()
    movie_list = movies['title'].values
except Exception as e:
    st.error("Backend Data Components mapping failed. Check absolute paths.")
    movie_list = ["Avatar", "Spectre", "Gladiator"]


def recommend(movie_name):
    # 1. Find the index of the movie the user selected in the dropdown
    movie_index = movies[movies['title'] == movie_name].index[0]
    
    # 2. Fetch the similarity scores for that specific movie index
    distances = similarity[movie_index]
    
    # 3. Sort them to find the top 5 closest matches (excluding the movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # 4. Extract the titles and TMDB IDs to send to the UI
    recommended_movies_titles = []
    recommended_movies_ids = []
    
    for i in movies_list:
        # Fetch ID for the API poster lookup
        recommended_movies_ids.append(movies.iloc[i[0]].movie_id)
        # Fetch title for the UI card layout
        recommended_movies_titles.append(movies.iloc[i[0]].title)
        
    return recommended_movies_titles, recommended_movies_ids


# ==========================================
# 4. SIDEBAR GRAPHICS COMPONENT
# ==========================================
with st.sidebar:
    st.markdown("## 🎬 About Project")
    st.markdown("""
    An AI-powered Movie Recommendation System that uses Natural Language Processing, CountVectorizer, and Cosine Similarity to discover movies with similar themes, genres, cast, and storylines.
    """)
    
    st.markdown("---")
    st.markdown("**Engine Architecture:**")
    st.markdown("• Python\n• Streamlit\n• Scikit-learn\n• CountVectorizer\n• Cosine Similarity")
    
    st.markdown("---")
    st.markdown("**Core Dataset Source:**\n\nTMDB 5000 Movies Dataset")
    
    st.markdown("---")
    st.markdown("<p style='color: #7C3AED; font-weight:600;'>Developer:</p><b>Ammar Gour</b>", unsafe_allow_html=True)


# ==========================================
# 5. CORE SYSTEM PRESENTATION
# ==========================================

# Rendering the top Hero Layout
st.markdown('<div class="hero-banner"></div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Find Movies You\'ll Enjoy Without The Hassle.</p>', unsafe_allow_html=True)

# Central Selection Mechanism Grid Block
col_select_left, col_select_mid, col_select_right = st.columns([1, 2, 1])

with col_select_mid:
    selected_movie = st.selectbox(
        label="Search Movie Database Directory",
        options=movie_list,
        label_visibility="collapsed",
        index=0
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    trigger_recommendation = st.button("🎥 Recommend Movies")

st.markdown("---")

# Intercept and execution response loops
if trigger_recommendation:
    with st.spinner("Finding similar movies..."):
        # Processing computation
        names, ids = recommend(selected_movie)
        st.toast("Recommendations Ready!", icon="✨")
        
        st.markdown('<h2 class="section-title">✨ Recommended Movies</h2>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Responsive 5-Column Horizontal Layout allocation Strategy
        columns = st.columns(5)
        
        for idx, col in enumerate(columns):
            if idx < len(names):
                with col:
                    # Async structural requests deployment mapping meta details safely
                    poster_url, year, score, genre = fetch_movie_meta(ids[idx])
                    
                    # Markdown component building the card template cleanly
                    card_html = f"""
                    <div class="movie-card">
                        <div class="poster-container">
                            <img src="{poster_url}" alt="{names[idx]}">
                        </div>
                        <div class="movie-info">
                            <div class="movie-card-title" title="{names[idx]}">{names[idx]}</div>
                            <div class="movie-meta-row">
                                <span>{year}</span>
                                <span class="rating-badge">★ {score}</span>
                            </div>
                            <div class="genre-tag">{genre}</div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)

# ==========================================
# 6. PREMIUM PLATFORM FOOTER
# ==========================================
st.markdown("""
    <div class="netflix-footer">
        <div class="footer-links">
            <a class="footer-link" href="https://github.com/AmmarGour" target="_blank">
                <i class="fab fa-github"></i> GitHub Portfolio
            </a>
            <a class="footer-link" href="https://linkedin.com/in/ammar-qasmi/-082266289" target="_blank">
                <i class="fab fa-linkedin"></i> LinkedIn Connect
            </a>
            <a class="footer-link" href="https://www.themoviedb.org/" target="_blank">
                🍿 TMDB Database
            </a>
            <a class="footer-link" href="#" target="_self">
                🛡️ Privacy Matrix
            </a>
        </div>
        <div class="footer-brand">CINEMATIC AI</div>
        <div class="footer-copyright">
            © 2026 Developed with Elite Core Logic by <b>Ammar Gour</b>. Powered by Cosine Similarity & Vector Embeddings.
        </div>
    </div>
""", unsafe_allow_html=True)
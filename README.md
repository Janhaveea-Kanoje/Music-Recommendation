# Music-Recommendation

# 🎵 Vibe Zone

*Where you listen to what you feel!*

Vibe Zone is a music recommendation system that helps you discover songs similar to your favorites. Built with machine learning and integrated with Spotify and YouTube, it provides an elegant interface to explore music based on lyrical content similarity.

## ✨ Features

- *Smart Recommendations*: Get song suggestions based on lyrical content similarity using TF-IDF and cosine similarity
- *Spotify Integration*: Fetch album covers, song metadata, and play tracks directly on Spotify
- *YouTube Integration*: Watch music videos embedded directly in the app
- *Beautiful UI*: Modern, responsive design with a beige/cream aesthetic
- *Search & Filter*: Find songs by name or artist, with sorting options
- *Paginated Browse*: Explore 5,000 songs with intuitive navigation

## 🚀 Demo

The app features:
- A hero section with elegant animations
- Grid-based song display with hover effects
- Detailed song pages with recommendations
- Integrated Spotify player and YouTube videos
- Match percentage for recommended songs

## 🛠 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

bash
git clone https://github.com/yourusername/vibe-zone.git
cd vibe-zone


### Step 2: Create a Virtual Environment (Recommended)

bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate


### Step 3: Install Dependencies

bash
pip install -r requirements.txt


### Step 4: Download NLTK Data

Open a Python shell and run:

python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')


### Step 5: Set Up Spotify API Credentials

1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Create a new app and get your Client ID and Client Secret
3. Open spotify_api.py and replace the placeholder credentials:

python
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"


Alternatively, set them as environment variables:

bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"


### Step 6: Prepare Model Files

The app requires two pickle files that should already be in the repository:
- df.pkl - Dataset of 5,000 songs
- similarity.pkl - Precomputed similarity matrix

If you need to regenerate these files, refer to the Model Training.ipynb notebook.

### Step 7: Run the Application

bash
streamlit run app.py


The app will open in your default browser at http://localhost:8501

## 📁 Project Structure
<img width="628" height="313" alt="image" src="https://github.com/user-attachments/assets/46aecaac-7948-4511-9d1c-c14da26ab9b4" />


## 🧠 How It Works

1. *Data Processing*: Song lyrics are preprocessed using tokenization and stemming (Porter Stemmer)
2. *Feature Extraction*: TF-IDF vectorization converts lyrics into numerical features
3. *Similarity Calculation*: Cosine similarity measures how similar songs are based on their lyrics
4. *Recommendations*: When you select a song, the system finds the most similar tracks
5. *Integration*: Spotify API fetches metadata and album art, YouTube API embeds videos

## 🎨 Technologies Used

- *Frontend*: Streamlit with custom CSS
- *Machine Learning*: scikit-learn (TF-IDF, Cosine Similarity)
- *NLP*: NLTK (tokenization, stemming)
- *APIs*: 
  - Spotipy (Spotify Web API)
  - YouTube (video embedding)
- *Data Processing*: Pandas, NumPy

## 📊 Dataset

The application uses a dataset of 5,000 songs sampled from a larger collection of 57,650 tracks. Each song includes:
- Artist name
- Song title
- Full lyrics

## 🔧 Configuration

You can customize various settings in config.py:
- Search limits
- Grid column counts
- UI colors and styling
- API timeouts
- Cache settings

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Known Issues

- YouTube video embedding may occasionally fail due to rate limiting
- Spotify API requires valid credentials to function
- Some songs may not have album art available

## 💡 Future Enhancements

- User authentication and saved playlists
- Audio feature-based recommendations (tempo, energy, etc.)
- Social features (share playlists, collaborative recommendations)
- Mobile app version
- Integration with more music platforms

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

*Made with ❤ and 🎵*

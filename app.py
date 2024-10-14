from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Spotify API Credentials
SPOTIFY_CLIENT_ID = 'bc93a10a093245ceb6d8610f0825ee86'
SPOTIFY_CLIENT_SECRET = '6f25a2ad278c4d04bb9b1f109be7f03d'

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyAr14gx7X5gK1YZrOde4X_F3BTqrhyk-F8"

# Lyrics.ovh for Lyrics API
LYRICS_API_URL = 'https://api.lyrics.ovh/v1'

# Free Dictionary API for word meanings
DICTIONARY_API_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

# Function to get Spotify token
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_data = {
        "grant_type": "client_credentials"
    }
    auth_response = requests.post(auth_url, auth_data, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
    return auth_response.json().get('access_token')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_spotify', methods=['POST'])
def search_spotify():
    query = request.form.get('query')
    token = get_spotify_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10"
    response = requests.get(search_url, headers=headers)
    data = response.json()

    tracks = []
    if data.get('tracks'):
        for item in data['tracks']['items']:
            tracks.append({
                'name': item['name'],
                'artist': item['artists'][0]['name'],
                'spotify_url': item['external_urls']['spotify'],
                'youtube_search_query': f"{item['name']} {item['artists'][0]['name']}"
            })
    return jsonify(tracks)

@app.route('/search_youtube', methods=['POST'])
def search_youtube():
    query = request.form.get('query')
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}&maxResults=1"
    response = requests.get(youtube_url)
    data = response.json()

    video_url = None
    if data.get('items'):
        video_id = data['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
    return jsonify({'video_url': video_url})

@app.route('/get_lyrics', methods=['POST'])
def get_lyrics():
    artist = request.form.get('artist')
    title = request.form.get('title')

    response = requests.get(f"{LYRICS_API_URL}/{artist}/{title}")
    if response.status_code == 200:
        data = response.json()
        lyrics = data.get('lyrics', 'Lyrics not found.')
    else:
        lyrics = 'Lyrics not found.'
    return jsonify({'lyrics': lyrics})

@app.route('/get_word_meaning', methods=['POST'])
def get_word_meaning():
    word = request.form.get('word')
    response = requests.get(f"{DICTIONARY_API_URL}{word}")
    
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and 'meanings' in data[0]:
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return jsonify({'meaning': definition})
    return jsonify({'meaning': 'No definition found'})

if __name__ == '__main__':
    app.run(debug=True)

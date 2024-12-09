import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API bilgilerinizi girin
client_id = '6ca7fbbd2e80456fa8e46225699bbbdc'
client_secret = '22e45d9962894bde9d1807de5fd3a9d2'

# Spotify API'ye bağlan
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Şarkı bilgilerini almak ve önerilerde bulunmak için fonksiyon
def get_song_features_and_recommendations(song_title):
    results = sp.search(q=song_title, limit=1, type='track')

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_id = track['id']
        features = sp.audio_features([track_id])[0]
        
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
        
        return track, features, recommendations['tracks']
    else:
        return None, None, None

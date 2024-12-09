

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Spotify API için kimlik bilgileri
spotify_client_id = '6ca7fbbd2e80456fa8e46225699bbbdc'  # Buraya kendi Spotify Client ID'nizi ekleyin
spotify_client_secret = '22e45d9962894bde9d1807de5fd3a9d2'  # Buraya kendi Spotify Client Secret'ınızı ekleyin

# Genius API için kimlik bilgileri
genius_api_key = '4KBzJjaPY1SStmY5jDlGLLpbOfVZlnnn_1K_dat_m4AdlCPU0gH1qCA4PPV05SEbs0J37ySa6-N7h0LifehShg'  # Buraya kendi Genius API Key'inizi ekleyin

def get_spotify_song(query):
    """Spotify'dan şarkı arama ve şarkı bilgilerini alma"""
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))
    results = sp.search(q=query, limit=5, type='track')
    if results['tracks']['items']:
        return [(track['name'], track['artists'][0]['name'], track['id']) for track in results['tracks']['items']]
    else:
        return []

def get_lyrics_from_genius(artist, song):
    """Genius API'den şarkı sözlerini alma"""
    genius = lyricsgenius.Genius(genius_api_key)
    song = genius.search_song(song, artist)
    if song:
        return song.lyrics
    return None

def compute_similarity(user_input, lyrics_list):
    """Kullanıcı kelimeleri ile şarkı sözleri arasındaki benzerliği hesaplama"""
    # Kullanıcıdan alınan kelimeler ile şarkı sözlerini karşılaştırmak için TF-IDF kullanacağız
    vectorizer = TfidfVectorizer().fit_transform([user_input] + lyrics_list)
    cosine_sim = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
    return cosine_sim

def get_most_similar_song(user_input, songs):
    """En benzer şarkıyı bulma"""
    lyrics_list = []
    for song_name, artist_name, _ in songs:
        lyrics = get_lyrics_from_genius(artist_name, song_name)
        if lyrics:
            lyrics_list.append(lyrics)
        else:
            lyrics_list.append("")

    # Benzerlik hesaplama
    similarity_scores = compute_similarity(user_input, lyrics_list)
    
    # En yüksek benzerlik skorunu bulan şarkıyı seçme
    max_sim_index = similarity_scores.argmax()
    most_similar_song = songs[max_sim_index]
    return most_similar_song, similarity_scores[max_sim_index]

def save_lyrics_to_json(song_name, artist_name, lyrics):
    """Tüm şarkı sözlerini tek bir JSON dosyasına kaydetme"""
    if not os.path.exists('songs.json'):
        with open('songs.json', 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    with open('songs.json', 'r+', encoding='utf-8') as file:
        data = json.load(file)
        song_data = {
            'song': song_name,
            'artist': artist_name,
            'lyrics': lyrics
        }
        data.append(song_data)
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Şarkı '{song_name}' - '{artist_name}' sözleri başarıyla 'songs.json' dosyasına kaydedildi.")

def main():
    """Ana program fonksiyonu"""
    user_input = input("Şarkı adı veya şarkı sözlerinden bir kısmı girin: ")

    # Spotify'dan şarkıları bulma
    songs = get_spotify_song(user_input)
    
    if songs:
        print(f"Spotify'da bulunan şarkılar:")
        for song_name, artist_name, _ in songs:
            print(f"- {song_name} - {artist_name}")

        # En benzer şarkıyı bulma
        most_similar_song, similarity_score = get_most_similar_song(user_input, songs)
        
        song_name, artist_name, _ = most_similar_song
        print(f"\nEn benzer şarkı: {song_name} - {artist_name} (Benzerlik Skoru: {similarity_score:.4f})")

        # Şarkı sözlerini alıp JSON dosyasına kaydetme
        lyrics = get_lyrics_from_genius(artist_name, song_name)
        if lyrics:
            save_lyrics_to_json(song_name, artist_name, lyrics)
        else:
            print("Şarkı sözleri bulunamadı.")
    else:
        print("Spotify'da şarkı bulunamadı.")

if __name__ == "__main__":
    main()

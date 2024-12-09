import lyricsgenius

# Genius API anahtarınızı buraya yazın
genius = lyricsgenius.Genius("4KBzJjaPY1SStmY5jDlGLLpbOfVZlnnn_1K_dat_m4AdlCPU0gH1qCA4PPV05SEbs0J37ySa6-N7h0LifehShg")

# Şarkı adı ve sanatçı ismiyle şarkı arama
def get_song_lyrics(song_title, artist_name):
    song = genius.search_song(song_title, artist_name)
    
    if song:
        return song.lyrics
    else:
        return None

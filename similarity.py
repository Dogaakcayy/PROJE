from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Kullanıcı girdisindeki kelimeleri ve şarkı sözlerini karşılaştıran fonksiyon
def get_most_similar_song(user_input, song_lyrics_list):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(song_lyrics_list + [user_input])

    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    most_similar_index = similarity_scores.argmax()
    return song_lyrics_list[most_similar_index]

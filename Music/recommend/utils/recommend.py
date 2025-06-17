from scipy.spatial.distance import cosine
from recommend.models import MusicEmbedding

# 유사도 계산

def get_all_embeddings():
    import numpy as np
    music_list = []
    for emb in MusicEmbedding.objects.select_related('music').all():
        music_list.append({
            'music_id': emb.music.id,
            'title': emb.music.title,
            'artist': emb.music.artist,
            'embedding': np.frombuffer(emb.embedding, dtype=np.float32),
        })
    return music_list

def recommend_similar_music(input_embedding, db_embeddings, top_k=5):
    similarities = []
    for item in db_embeddings:
        sim = 1 - cosine(input_embedding, item['embedding'])
        similarities.append((item['music_id'], item['title'], item['artist'], sim))
    similarities.sort(key=lambda x: x[3], reverse=True)
    return similarities[:top_k]

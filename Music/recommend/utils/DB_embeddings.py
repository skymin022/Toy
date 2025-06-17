from scipy.spatial.distance import cosine

def recommend_similar_music(input_embedding, db_embeddings, top_k=5):
    similarities = []
    for item in db_embeddings:
        sim = 1 - cosine(input_embedding, item['embedding'])
        similarities.append((item['music_id'], item['title'], sim))
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:top_k]

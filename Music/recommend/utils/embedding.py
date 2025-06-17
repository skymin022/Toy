import numpy as np
from recommend.model.generator import generator_model

# 임베딩 추출
generator = generator_model()
generator.load_weights('generator_pretrain.h5')  # ✅ 올바른 예시

def extract_embedding(midi_input):
    embedding = generator.predict(midi_input)
    return embedding.flatten()

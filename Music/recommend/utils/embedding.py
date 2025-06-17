import numpy as np
from recommend.model.generator import generator_model

# 임베딩 추출
generator = generator_model()
generator.load_weights('generator_pretrain')  # 실제 경로로 수정

def extract_embedding(midi_input):
    embedding = generator.predict(midi_input)
    return embedding.flatten()

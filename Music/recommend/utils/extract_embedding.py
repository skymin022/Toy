import numpy as np

# 모델 로딩
generator = generator_model()
generator.load_weights('generator_pretrain')  # 사전학습 가중치 필요

def extract_embedding(midi_input):
    # midi_input: (batch, time, features) 형태
    embedding = generator.predict(midi_input)
    # 중간 레이어 출력을 임베딩으로 사용할 수도 있음
    return embedding.flatten()

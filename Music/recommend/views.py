from django.shortcuts import render, redirect
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os

# 1. 키워드로 유튜브 영상 검색
def search_view(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        videos_search = VideosSearch(keyword, limit=10)
        video_list = []
        for video in videos_search.result()['result']:
            video_list.append({
                'title': video['title'],
                'url': video['link'],
                'duration': video['duration'],
                'thumbnails': video['thumbnails'][0]['url'],
            })
        return render(request, 'recommend/select.html', {'video_list': video_list})
    return render(request, 'recommend/search.html')

# 2. 영상 선택 → 음원 추출
def select_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        # 음원 추출
        audio_path = download_audio_from_youtube(video_url)
        # 전처리 (예시)
        input_tensor = preprocess_audio(audio_path)
        # 이후 추천 파이프라인 연결 (여기서는 결과만 출력)
        return render(request, 'recommend/result.html', {'audio_path': audio_path})
    return redirect('search')

# 3. 결과 페이지 (추후 추천 결과 등 표시)
def result_view(request):
    return render(request, 'recommend/result.html')

# --- 유틸 함수 ---

def download_audio_from_youtube(url, output_path='media', filename='input.mp3'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download(output_path=output_path, filename=filename)
    return os.path.join(output_path, filename)

import librosa
import numpy as np

def preprocess_audio(audio_path, sr=22050, n_mels=128, hop_length=512, duration=5, seq_len=10):
    y, _ = librosa.load(audio_path, sr=sr, duration=duration)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, hop_length=hop_length)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_spec_norm = (mel_spec_db - mel_spec_db.min()) / (mel_spec_db.max() - mel_spec_db.min() + 1e-6)
    total_frames = mel_spec_norm.shape[1]
    frames_per_seq = total_frames // seq_len
    slices = []
    for i in range(seq_len):
        start = i * frames_per_seq
        end = start + frames_per_seq
        if end > total_frames:
            break
        slices.append(mel_spec_norm[:, start:end])
    slices = np.stack(slices, axis=0)
    slices = slices[..., np.newaxis]
    return slices  # (seq_len, n_mels, frames_per_seq, 1)


# 파이프 라인 cnn-lstm

def recommend_view(request):
    if request.method == 'POST':
        midi_file = request.FILES['midi']
        midi_input = midi_to_model_input(midi_file)  # MIDI → 모델 입력 변환 함수
        input_embedding = extract_embedding(midi_input)
        db_embeddings = get_all_embeddings()  # DB에서 임베딩 불러오기
        recommendations = recommend_similar_music(input_embedding, db_embeddings)
        return render(request, 'recommend/result.html', {'recommendations': recommendations})
    return render(request, 'recommend/upload.html')

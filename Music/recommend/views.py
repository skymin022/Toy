from django.shortcuts import render, redirect
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os
from recommend.utils.audio_processing import audio_to_midi, midi_to_model_input
from recommend.utils.embedding import extract_embedding
from recommend.utils.recommend import get_all_embeddings, recommend_similar_music

MEDIA_ROOT = 'media'

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

def select_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        try:
            audio_path = download_audio_from_youtube(video_url)
            midi_path = audio_to_midi(audio_path)
            midi_input = midi_to_model_input(midi_path)
            input_embedding = extract_embedding(midi_input)
            db_embeddings = get_all_embeddings()
            recommendations = recommend_similar_music(input_embedding, db_embeddings)
            # 파일 정리 (보안/용량 관리)
            safe_remove(audio_path)
            safe_remove(midi_path)
            return render(request, 'recommend/result.html', {'recommendations': recommendations})
        except Exception as e:
            return render(request, 'recommend/result.html', {'error': str(e)})
    return redirect('search')

def download_audio_from_youtube(url, output_path=MEDIA_ROOT, filename='input.mp3'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    if not stream:
        raise Exception('오디오 스트림을 찾을 수 없습니다.')
    file_path = os.path.join(output_path, filename)
    stream.download(output_path=output_path, filename=filename)
    return file_path

def safe_remove(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


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

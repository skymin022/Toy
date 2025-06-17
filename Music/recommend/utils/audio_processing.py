import pretty_midi
import tempfile
import os

# 오디오 ➡ MIDI 변환
def audio_to_midi(audio_path):
    # 실제 변환은 복잡하므로 예시로 임시 파일 반환
    # 실전에서는 spleeter, demucs 등으로 보컬/멜로디 추출 후 변환
    midi_path = audio_path.replace('.wav', '.mid')
    # 변환 로직 구현 필요
    return midi_path

def midi_to_model_input(midi_file):
    # MIDI 파일을 numpy 배열 등 모델 입력 형태로 변환
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    # 예시: 피아노롤 변환
    piano_roll = midi_data.get_piano_roll(fs=100)
    # shape 맞추기
    model_input = piano_roll.T[:100, :1]  # (100, 1)
    model_input = model_input.reshape(1, 100, 1)
    return model_input

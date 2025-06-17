from django.db import models


# DB 모델 관리
class Music(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    # 기타 메타데이터 필드

class MusicEmbedding(models.Model):
    music = models.OneToOneField(Music, on_delete=models.CASCADE)
    embedding = models.BinaryField()  # numpy array bytes로 저장

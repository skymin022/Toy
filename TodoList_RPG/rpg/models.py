# rpg/models.py

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORY_LEVELS = (
        (1, '대분류'),
        (2, '중분류'),
        (3, '소분류'),
    )
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=CATEGORY_LEVELS, default=1)

    def __str__(self):
        return self.name

class Stat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 대분류별 점수(예: 공부, 운동, 체력 등)
    # 예시: 공부, 운동, 체력, 외모, 재력
    # 실제로는 Category와 연동하여 동적으로 생성 가능
    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

class UserCategoryStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    achieved = models.BooleanField(default=False)
    date_achieved = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"
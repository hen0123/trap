import os

from django.db import models

# Create your models here.
from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()


### 보관함 모델
class Mypothole(models.Model):

    # 영상 생성 제목 - 신고 제목
    title = models.CharField(max_length=200, default=datetime.now().strftime("%Y%m%d_%H%M%S_%f"))

    # 발생 위치(좌표) / lat:위도, long:경도
    lat = models.CharField(max_length=30, null=True, blank=True, default=37.4765)
    long = models.CharField(max_length=30, null=True, blank=True, default=126.9816)

    # 감지 날짜
    detect_date = models.DateTimeField(auto_now_add=True)

    # 감지 이미지/영상
    detect_file = models.ImageField(upload_to='upload', null=False, blank=False)

    # 글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE)



    # 제목으로 표시
    def __str__(self):
        return self.title


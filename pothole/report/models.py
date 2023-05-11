from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# 신고 게시판 - 신고(질문) 모델

class Report(models.Model):
    # 신고 제목
    subject = models.CharField(max_length=200)

    # 신고 위치(좌표) / x:위도, y:경도
    x_pos = models.CharField(max_length=30)
    y_pos = models.CharField(max_length=30)

    # 신고 내용
    content = models.TextField()

    # 신고 날짜
    create_date = models.DateTimeField(auto_now_add=True)

    # 첨부파일
    file = models.FileField(upload_to='report', null=True, blank=True)

    # 처리 상황
    state = models.CharField(max_length=10, default="접수완료")

    # 글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE)



    # 제목으로 표시
    def __str__(self):
        return self.subject

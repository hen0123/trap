from django.db import models
from django.contrib.auth import get_user_model


# user 확장
# (id, 비밀번호, 이메일, 이름, 전화번호)

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):

    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=13)
    email = models.EmailField()


# 위치 중요!!! 무조건 class보다 아래에 있어야 함!
User = get_user_model()
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
User = get_user_model()

# 회원가입 시 입력 목록 : username, password, name, phone, email
class UserForm(UserCreationForm):

    name = forms.CharField(label="이름")
    phone = forms.CharField(label="전화번호")
    email = forms.EmailField(label="이메일")

    class Meta(UserCreationForm):

        model = User
        fields = ("username", "password1", "password2",  "name", "phone", "email")

# mypage 정보수정
class UpdateUserForm(forms.ModelForm):
    #username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=13, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ("name", "phone", "email")


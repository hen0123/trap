from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login
from .forms import UserForm, UpdateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

# 메인페이지
def index(request):
    return render(request, 'common/main.html')

# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

# 마이페이지
@login_required
def mypage(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)


        if user_form.is_valid():
            user_form.save()
            return redirect(to='common:mypage')

    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'common/mypage.html', {'user_form': user_form})



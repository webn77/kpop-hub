from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import SignupForm, ProfileEditForm

User = get_user_model()


def signup_view(request):
    """회원가입."""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'환영합니다, {user.nickname or user.username}님!')
            return redirect('/')
        else:
            messages.error(request, '입력 정보를 확인해 주세요.')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """로그인."""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'로그인했습니다, {user.nickname or user.username}님!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """로그아웃 (POST만 허용)."""
    if request.method == 'POST':
        logout(request)
        messages.success(request, '로그아웃했습니다.')
    return redirect('/')


@login_required
def profile_view(request):
    """프로필 조회 / 수정."""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 수정되었습니다.')
            return redirect('accounts:profile')
        else:
            messages.error(request, '입력 정보를 확인해 주세요.')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})

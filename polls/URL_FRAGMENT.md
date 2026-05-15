# polls URL Fragment
# config/urls.py에 아래 패턴을 추가하세요.

path('polls/', include('polls.urls', namespace='polls')),

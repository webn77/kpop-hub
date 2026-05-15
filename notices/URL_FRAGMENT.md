# notices URL Fragment

config/urls.py urlpatterns에 추가할 패턴:

```python
path('notices/', include('notices.urls', namespace='notices')),
```

추가 위치: config/urls.py의 urlpatterns 리스트 안,
accounts/ 패턴 아래에 삽입.

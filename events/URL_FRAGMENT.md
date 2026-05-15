# events 앱 URL 등록 안내

config/urls.py에 아래 패턴을 추가하세요.

## 추가할 import

```python
from django.urls import path, include
```

## urlpatterns에 추가할 항목

```python
path('events/', include('events.urls', namespace='events')),
```

## 전체 예시 (config/urls.py)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('events/', include('events.urls', namespace='events')),  # ← 추가
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 주의사항

- events/urls.py에 `app_name = 'events'`가 이미 선언되어 있습니다.
- namespace와 app_name이 일치해야 템플릿의 `{% url 'events:list' %}` 등이 정상 동작합니다.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin 사이트 커스터마이징
admin.site.site_header = "KPOP HUB 관리자"
admin.site.site_title = "KPOP HUB"
admin.site.index_title = "관리자 대시보드"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('notices/', include('notices.urls', namespace='notices')),
    path('events/', include('events.urls', namespace='events')),
    path('polls/', include('polls.urls', namespace='polls')),
    path('surveys/', include('surveys.urls', namespace='surveys')),
    path('search/', include('search.urls', namespace='search')),
    path('', include('posts.urls', namespace='posts')),        # 메인 = 게시판
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# posts URL Fragment

config/urls.py에 추가할 패턴:

```python
path('posts/', include('posts.urls', namespace='posts')),
```

## 선택 근거
- `posts/` prefix 사용 (task plan의 `path('')` 대신)
- base.html 네비게이션이 `/posts/` 하드코딩된 링크를 사용하므로 일치
- Django 관례: 앱 URL은 접두사를 포함해 마운트

## 최종 config/urls.py urlpatterns 형태
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('posts/', include('posts.urls', namespace='posts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## posts 앱 내부 URL 목록
| URL | name | view |
|-----|------|------|
| /posts/ | posts:list | PostListView |
| /posts/<pk>/ | posts:detail | PostDetailView |
| /posts/create/ | posts:create | PostCreateView |
| /posts/<pk>/update/ | posts:update | PostUpdateView |
| /posts/<pk>/delete/ | posts:delete | PostDeleteView |
| /posts/<pk>/like/ | posts:like | PostLikeView (HTMX) |
| /posts/<pk>/comment/ | posts:comment_create | CommentCreateView (HTMX) |
| /posts/comment/<pk>/delete/ | posts:comment_delete | CommentDeleteView |

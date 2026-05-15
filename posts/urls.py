from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # 목록
    path('', views.PostListView.as_view(), name='list'),
    # 상세
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    # 작성
    path('create/', views.PostCreateView.as_view(), name='create'),
    # 수정
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),
    # 삭제
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    # 좋아요 (HTMX)
    path('<int:pk>/like/', views.PostLikeView.as_view(), name='like'),
    # 댓글 작성 (HTMX)
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    # 댓글 삭제
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]

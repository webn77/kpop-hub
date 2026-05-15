from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.PollListView.as_view(), name='list'),
    path('<int:pk>/', views.PollDetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.PollVoteView.as_view(), name='vote'),
    path('<int:pk>/result/', views.PollResultView.as_view(), name='result'),
]
